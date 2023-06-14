import csv
import random

def generate_dot_file(data, clan_data):
    dot_file = "family_tree.dot"

    with open(dot_file, "w") as file:
        file.write("digraph FamilyTree {\n")
        file.write('    node [shape=box]\n\n')

        clan_map = {}

        # Create a mapping of clan IDs to unique background colors
        for clan in clan_data:
            clan_id = clan['clanId']
            clan_name = clan['clanName']
            color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
            clan_map[clan_id] = {'name': clan_name, 'color': color}

        for person in data:
            pid = person['pid']
            name = person['name']
            gender = person['gender']
            generation = person['generation']
            byear = person['byear']
            dyear = person['dyear']
            dage = person['dage']
            myear = person['myear']
            mage = person['mage']
            ptype = person['ptype']
            clan_id = person['clan']
            spouse_id = person['spouseId']
            parent_id1 = person['parentId1']
            parent_id2 = person['parentId2']
            parent_node_id = person['parentNodeId']

            # Retrieve the clan details based on clan ID from the clan map
            clan_details = clan_map.get(clan_id, {'name': "Unknown Clan", 'color': "#FFFFFF"})

            # Set the shape based on gender
            shape = "box"
            if gender == "Female":
                shape = "ellipse"

            # Write node information with clan name, shape, and color
            file.write(f'    {pid} [label="Name: {name}\\nGender: {gender}\\nGeneration: {generation}\\n{byear}-{dyear} ({dage})\\nClan: {clan_details["name"]}", shape={shape}, style=filled, fillcolor="{clan_details["color"]}"]\n')

            # Write edge information for spouse
            if spouse_id != "":
                file.write(f'    {pid} -> {spouse_id} [label="spouse"]\n')

            # Write edge information for parents
            if parent_id1 != "":
                file.write(f'    {parent_id1} -> {pid} [label="child"]\n')
            if parent_id2 != "":
                file.write(f'    {parent_id2} -> {pid} [label="child"]\n')

            

        file.write("}")

    print(f"DOT file '{dot_file}' generated successfully!")


# Read data from CSV files
def read_csv_data(filename):
    data = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return data


# Example usage with CSV files
csv_filename = "Family_data.csv"
clan_csv_filename = "Clan_data.csv"
family_data = read_csv_data(csv_filename)
clan_data = read_csv_data(clan_csv_filename)
generate_dot_file(family_data, clan_data)
