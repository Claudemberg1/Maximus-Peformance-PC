Maximus PC Performance
O Maximus PC Performance é uma ferramenta de otimização de sistema desenvolvida em Python para o ambiente Windows. O software centraliza diversas rotinas de manutenção e ajustes de desempenho, desde a limpeza de arquivos residuais até a configuração de prioridades de hardware para jogos e aplicações pesadas.

Funcionalidades principais
O software oferece um painel com as seguintes opções:

Limpeza de arquivos temporários: Remoção de caches de usuário, arquivos temporários do Windows, Prefetch e limpeza automática da lixeira para liberação de RAM e espaço em disco.

Atualização de sistema e drivers: Interface para forçar a busca de atualizações do Windows Update.

Atualização de programas (Winget): Utiliza o gerenciador de pacotes do Windows para atualizar todos os softwares instalados para suas versões mais recentes.

Otimização de desempenho: Ajusta o plano de energia para desempenho máximo (em desktops) e modifica chaves de registro para melhorar a responsividade da CPU.

Modo Gamer Extremo: Desativa serviços de telemetria, encerra o OneDrive e define prioridade máxima de GPU e rede para processos de jogos.

Restauração do sistema: Reverte as alterações de serviços e registros para os padrões originais de estabilidade do Windows.

Manual de uso: Acesso direto ao manual de performance em PDF embutido no software.

Sistema de Licenciamento
O software possui uma camada de segurança integrada:

ID Único: Gera um identificador baseado no nome do computador e do usuário.

Validação Online: Verifica a chave de ativação através de uma API conectada ao Google Apps Script.

Persistência Local: Armazena um arquivo de licença criptografado para evitar a necessidade de ativação a cada inicialização, desde que o hardware permaneça o mesmo.

Requisitos de Instalação
Para rodar o código fonte, é necessário ter o Python 3.x instalado e as seguintes bibliotecas:

Bash
pip install Pillow requests
Compilação para Executável
Para gerar o arquivo .exe utilizando o PyInstaller, mantendo os arquivos externos (GIF e PDF) dentro do executável, utilize o comando:

Bash
pyinstaller --noconfirm --onefile --windowed --add-data "loading.gif;." --add-data "Maximus_PC_Performance_Manual.pdf;." seu_script.py
Notas Técnicas
Privilégios: O software requer execução como Administrador para realizar alterações no Registro do Windows e gerenciar serviços do sistema.

Segurança: As alterações de registro são focadas em Win32PrioritySeparation e priorização de tarefas multimídia para reduzir latência.

Interface: Desenvolvida em Tkinter com suporte a processamento em segundo plano (threading) para manter a interface responsiva durante as otimizações.

Tecnologias Utilizadas
Linguagem: Python

Interface Gráfica: Tkinter

Processamento de Imagem: PIL (Pillow)

Comunicação: Requests e Socket

Integração de Sistema: Subprocess, OS, Shutil e Ctypes