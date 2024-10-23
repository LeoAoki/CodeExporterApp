import os
import json

# Lista padrão de diretórios ignorados
DEFAULT_IGNORED_DIRS = [
    ".git", "bin", "obj", "node_modules", "venv", ".idea", ".vscode",
    ".vs", "dist", "target", ".gradle", ".next", "build", "__pycache__",
    "coverage", ".cache", ".pytest_cache", ".parcel-cache", ".nuget",
    "logs", "lib", "tmp", "docker",".sass-cache", "public", "vendor",
    ".DS_Store", "Thumbs.db"
]

# Função para gerar a árvore de diretórios de cada projeto especificado
def generate_directory_tree(project_dirs, ignored_dirs):
    tree = []
    for project_dir in project_dirs:
        project_name = os.path.basename(os.path.normpath(project_dir))
        
        if not os.path.exists(project_dir):
            tree.append(f"• Diretório {project_name} não encontrado.\n")
            continue
        
        tree.append(f"• Estrutura do projeto {project_name}:\n")
        for dirpath, dirnames, filenames in os.walk(project_dir):
            dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
            
            level = dirpath.replace(project_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            tree.append(f'{indent}{os.path.basename(dirpath)}/')
            sub_indent = ' ' * 4 * (level + 1)
            for filename in filenames:
                tree.append(f'{sub_indent}{filename}')
        tree.append("")
    return '\n'.join(tree)

# Função para resolver o caminho absoluto do arquivo
def resolve_file_path(file_path, project_dirs):
    for project_dir in project_dirs:
        project_name = os.path.basename(os.path.normpath(project_dir))
        if file_path.startswith(project_name):
            relative_path = file_path[len(project_name)+1:]
            absolute_path = os.path.join(project_dir, relative_path)
            if os.path.exists(absolute_path):
                return absolute_path, project_name
    raise ValueError(f"O arquivo {file_path} não foi encontrado em nenhum dos projetos especificados.")

# Função para ler e exportar arquivos escolhidos
def export_files(file_paths, project_dirs):
    exported_content = []
    
    for file_path in file_paths:
        try:
            absolute_file_path, project_name = resolve_file_path(file_path, project_dirs)
            
            with open(absolute_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            exported_content.append(f"• {file_path}:\n\n{content}\n")
        
        except ValueError as e:
            exported_content.append(f"• Erro: {e}\n")
    
    return '\n'.join(exported_content)

# Função principal que gera o TXT com a árvore e os arquivos exportados
def create_export(project_dirs, file_paths, ignored_dirs, output_file="project_export.txt"):
    tree = generate_directory_tree(project_dirs, ignored_dirs)
    
    if file_paths:
        file_content = export_files(file_paths, project_dirs)
        export_text = f"{tree}\n****** Arquivos exportados: ******\n\n{file_content}"
    else:
        export_text = f"{tree}\n****** Nenhum arquivo exportado. ******\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(export_text)

    print(f"Exportação concluída! Arquivo salvo como {output_file}")

# Função para carregar o config.json
def load_config(config_file="config.json"):
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            if 'projects' not in config or not isinstance(config['projects'], list) or len(config['projects']) == 0:
                raise ValueError("O arquivo config.json deve conter ao menos um diretório na chave 'projects'.")
            
            file_paths = config.get('files', [])

            ignored_dirs = config.get('ignored_dirs', DEFAULT_IGNORED_DIRS)
            
            return config['projects'], file_paths, ignored_dirs
        
        except json.JSONDecodeError:
            raise ValueError("Erro ao analisar o arquivo config.json. Verifique se ele está formatado corretamente.")
    else:
        raise FileNotFoundError(f"Arquivo {config_file} não encontrado. Certifique-se de que ele existe na raiz do projeto.")

if __name__ == "__main__":
    try:
        project_dirs, file_paths, ignored_dirs = load_config()

        create_export(project_dirs, file_paths, ignored_dirs)
    
    except Exception as e:
        print(f"Erro: {e}")