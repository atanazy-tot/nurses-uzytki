import os

def create_neos_xml(mod_file_path, dat_file_path, sol_file_path, output_xml_path):
    with open(mod_file_path, 'r') as mod_file:
        mod_content = mod_file.read()

    with open(dat_file_path, 'r') as dat_file:
        dat_content = dat_file.read()

    with open(sol_file_path, 'r') as sol_file:
        sol_content = sol_file.read()

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<document>
  <category>kestrel</category>
  <solver>baron</solver>
  <inputMethod>GAMS</inputMethod>
  <model><![CDATA[{mod_content}]]></model>
  <data><![CDATA[{dat_content}]]></data>
  <commands><![CDATA[{sol_content}]]></commands>
</document>
"""

    with open(output_xml_path, 'w') as xml_file:
        xml_file.write(xml_content)

mod_file_path = 'project3.mod'
dat_file_path = 'dat_files/first_data.dat'
sol_file_path = 'command.sol'
output_xml_path = 'xml_files/first_output.xml'

create_neos_xml(mod_file_path, dat_file_path, sol_file_path, output_xml_path)

print(f"XML file created at {output_xml_path}")