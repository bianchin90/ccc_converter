import os

#put here list of files
files = ['TEST.edl',
         'TEST2.edl',
         'TEST3.edl']

#insert path
for file_path in files :
#file_path = 'TEST.edl'

    #read file
    input_file = open(file_path, 'r')

    #get file name
    file_name = os.path.splitext(file_path)[0]

    #create output file
    output_file_name = "./CCC_FILES/{0}.ccc".format(file_name)
    if not os.path.exists(os.path.dirname(output_file_name)):
        os.makedirs(os.path.dirname(output_file_name))
    output = open(output_file_name, "w")
    output.write('<ColorCorrectionCollection xmlns="urn:ASC:CDL:v1.01">\n')

    for line in input_file:
        #if line.startswith('0000'):
        if line[0].isnumeric():

            # repeating tags
            #get id
            line = line.replace(' ','')
            id = line[6:].split('VC')[0]
            output.write('		<ColorCorrection id="{0}">\n'.format(id))
            output.write('			<SOPNode>\n')

        #slope, offset and power
        if line.startswith('*ASC_SOP'):
            slope = line.split('(')[1].split(')')[0]
            offset = line.split(')(')[1].split(')(')[0]
            power = line.split(')(')[2].split(')')[0]

            output.write('				<Description></Description>\n')
            output.write('				<Slope>{0}</Slope>\n'.format(slope))
            output.write('				<Offset>{0}</Offset>\n'.format(offset))
            output.write('				<Power>{0}</Power>\n'.format(power))
            output.write('			</SOPNode>\n')

        #sat
        if line.startswith('*ASC_SAT'):
            sat = line.split('*ASC_SAT')[1].rstrip()
            if sat.startswith(' ') : sat = sat[1:]
            output.write('				<SATNode>\n')
            output.write('					<Saturation>{0}</Saturation>\n'.format(sat))
            output.write('				</SATNode>\n')
            output.write('		</ColorCorrection>\n')

    #closing line
    output.write('</ColorCorrectionCollection>')
    output.close()
    print("file {0}.edl saved to file {0}.ccc".format(file_name))