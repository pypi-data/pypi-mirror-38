#
# Example Julia conversion script
#
# September  2, 2016 -- Andreas Scheidegger
# -------------------------------------------------------

# here the module name does not match the file name:

module non_ascii_output

using DelimitedFiles
using Dates

# the function name must be covert:

function convert(rawfile, outputfile)

    raw = DelimitedFiles.readdlm(rawfile, '\t', skipstart=2)

    dat = [Dates.DateTime(str, "dd.mm.yyyy HH:MM") for str in raw[:,1]]

    # write file (Should be in standardizes file format. This is not the case here.)
    final = hcat(dat, raw[:,2])

    # introduce non ascii characters
    final[1, 1] = "äää"

    writedlm(outputfile, final, ';')
end

end
