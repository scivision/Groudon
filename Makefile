# For clean up and build up binary code
#
#

gr: grwave/grwave.for
	$(FC) -o $@ $<

clean:
	@- $(RM) *.pyc
	@- $(RM) KM
	@- $(RM) inp*
	@- $(RM) out*
	@- $(RM) BPL
	@- $(RM) -rf millington_file


