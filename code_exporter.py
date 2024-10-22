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

# Função para verificar se um arquivo está dentro de algum dos diretórios do projeto
def is_file_within_project(file_path, project_dirs):
    for project_dir in project_dirs:
        if os.path.commonpath([file_path, project_dir]) == os.path.normpath(project_dir):
            relative_path = os.path.relpath(file_path, start=os.path.dirname(project_dir))
            return True, relative_path
    return False, None

# Função para ler e exportar arquivos escolhidos, exibindo caminho relativo ao projeto
def export_files(file_paths, project_dirs):
    exported_content = []
    for file_path in file_paths:
        file_path = os.path.normpath(file_path)
        valid, relative_path = is_file_within_project(file_path, project_dirs)
        
        if not valid:
            raise ValueError(f"Erro: O arquivo {file_path} não está dentro de nenhum dos diretórios do projeto.")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            exported_content.append(f"• {relative_path}\n\n{content}\n")
        except Exception as e:
            exported_content.append(f"• {relative_path}\n\nError reading file: {e}\n")
    return '\n'.join(exported_content)

# Função principal que gera o TXT com a árvore e os arquivos exportados
def create_export(project_dirs, file_paths, ignored_dirs, output_file="project_export.txt"):

    tree = generate_directory_tree(project_dirs, ignored_dirs)

    file_content = export_files(file_paths, project_dirs)

    export_text = f"****** Projetos: ******\n\n{tree}\n****** Arquivos exportados: ******\n\n{file_content}"

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
                raise ValueError("O arquivo config.json deve conter uma lista de diretórios na chave 'projects'.")
            
            if 'files' not in config or not isinstance(config['files'], list) or len(config['files']) == 0:
                raise ValueError("O arquivo config.json deve conter uma lista de arquivos na chave 'files'.")
            
            # Se a chave 'ignored_dirs' não estiver presente, usa a lista padrão
            ignored_dirs = config.get('ignored_dirs', DEFAULT_IGNORED_DIRS)
            
            return config['projects'], config['files'], ignored_dirs
        
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