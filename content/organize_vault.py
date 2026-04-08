import os
import re

root = '/home/yash/vault/content'

for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith('.md'):
            filepath = os.path.join(dirpath, filename)
            print(f"Processing {filepath}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.split('\n')
            frontmatter_end = -1
            if lines and lines[0] == '---':
                for i in range(1, len(lines)):
                    if lines[i] == '---':
                        frontmatter_end = i
                        break
            if frontmatter_end > 0:
                frontmatter_lines = lines[1:frontmatter_end]
                data = {}
                for line in frontmatter_lines:
                    if ': ' in line:
                        key, value = line.split(': ', 1)
                        if key == 'tags':
                            # assume [tag1, tag2]
                            value = value.strip('[]').split(', ')
                            data[key] = [v.strip() for v in value if v.strip()]
                        else:
                            data[key] = value
            else:
                data = {}
                frontmatter_end = 0

            # Set title if not present
            if 'title' not in data or not data['title'].strip():
                title = filename[:-3]  # remove .md
                data['title'] = title

            # Add tags based on path
            rel_path = os.path.relpath(dirpath, root)
            if rel_path == '.':
                folders = []
            else:
                folders = rel_path.split(os.sep)
            tags = []
            for folder in folders:
                # Clean folder name: remove leading digits and dots, replace spaces with hyphens, lowercase
                clean_tag = re.sub(r'^\d+\.\s*', '', folder).replace(' ', '-').replace('_', '-').lower()
                if clean_tag and clean_tag not in tags:
                    tags.append(clean_tag)
            if tags:
                if 'tags' not in data:
                    data['tags'] = tags
                else:
                    existing_tags = set(data['tags']) if isinstance(data['tags'], list) else set()
                    for tag in tags:
                        if tag not in existing_tags:
                            data['tags'].append(tag)

            # Build frontmatter
            frontmatter = f"title: {data['title']}\n"
            if 'tags' in data and data['tags']:
                tags_str = ', '.join(data['tags'])
                frontmatter += f"tags: [{tags_str}]\n"
            if 'date' in data:
                frontmatter += f"date: {data['date']}\n"
            # add other fields if present

            # Write back
            if frontmatter_end > 0:
                new_content = '---\n' + frontmatter + '---\n' + '\n'.join(lines[frontmatter_end + 1:])
            else:
                new_content = '---\n' + frontmatter + '---\n' + content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

print("Vault organization complete.")


