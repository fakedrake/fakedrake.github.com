title: Ethernet deadlocks and forking the kernel
date: 2014-07-16 18:25
tags: drivers, irq, linux, kernel
category: kernel
slug: ethernet-deadlocks-and-forking-the-kernel
author: Chris Perivolaropoulos
summary: A case study of fixing an irq deadlock in the linux kernel.

This is a bit specific but it is something I encountered more than
once and spent a couple of hours trying to fix. So here is the
problem. I have a xilinx zynq zc702 board and I load a slightly
customized 3.8 linux kernel on it. I boot it and it freezes at

	loop: module loaded
	xqspips e000d000.spi: master is unqueued, this is deprecated

Now now you probably want to know what boot arguments I was using and
what kind of modifications I have made to the kernel and the exact
release but it doesn't really matter. The problem was the xqspips
driver and not the fact that something is deprecated -who knows what
this message means exactly-.

Let me walk you through around the problem what happens in
[drivers/spi/spi-xilinx-qps.c](https://github.com/fakedrake/linux-thinksilicon/blob/qemu/drivers/spi/spi-xilinx-qps.c)
when a spi transfer commences.

- `xqspips_start_transfer` runs
- At some poiunt it writes to `XQSPIPS_IEN_OFFSET` register to raise
  an interrupt that will call asynchronously `xqspips_irq`
- `xqspips_start_transfer` inits some other stuff and then waits for
  `xqspips_irq` to set a completion structure.

Now `xqspips_irq` is passed a `xqspips` structure that contains
information about how much data we want to transmit and how much data
we expect to receive.

- First it checks with the status register to see if there is some
  space in the transfer buffer or that there is something useful in
  the receive buffer.
- While the receive buffer is not empty try to read data from it
  decrementing `struct xqspips->bytes_to_receive` correctly.
- If there is stuff to transfer, transfer it
- If `struct xqspips->bytes_to_receive` is not yet zero reissue an
  interrupt in a slightly different way than before and finalize.
- If `struct xqspips->bytes_to_receive` is zero complete the
  completion struct that `xqspips_start_transfer` is waiting for and
  finalize.

The above is a rough descriuption of the situation. Now I don't know
if it is a hardware problem or a driver bug but there are two problems
here. One is that `xqspi->bytes_to_receive` is 1 while the status
register claims there is no data in the buffer. And also setting the
`IEN` register doesn't raise an interrupt. Thus irq callback fails to
read the data isntructed by `xqspi->bytes_to_receive` and proceeds
finish confident that an interrupt was raised to take care of the
situation.

The hard part of this was finding all the above out. Then it was
trivial to just tell `xqspips_irq` to not only check the status
register to decide whether it should read or not, but also check with
the xqspi struct. Essentially changing


	:::C
	/* Read out the data from the RX FIFO */
	while (xqspips_read(xqspi->regs + XQSPIPS_STATUS_OFFSET) &
		XQSPIPS_IXR_RXNEMTY_MASK) {

into


	:::C
	/* Read out the data from the RX FIFO */
	while ((xqspips_read(xqspi->regs + XQSPIPS_STATUS_OFFSET) &
		XQSPIPS_IXR_RXNEMTY_MASK) ||
		xqspi->bytes_to_receive) {

did the trick.
