# For clean up and build up binary code
#
#

gr: grwave/grwave.for
	$(FC) -o $@ $< -g -fbacktrace

clean:
	$(RM) gr
	$(RM) KM
	$(RM) inp*
	$(RM) out*
	$(RM) BPL
	$(RM) -r millington_file


