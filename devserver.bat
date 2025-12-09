@echo off
REM Se .venv nao existir, criar e instalar dependencias
if not exist ".venv\Scripts\activate.bat" (
	echo Virtualenv nao encontrada. Criando .venv...
	python -m venv .venv
	if errorlevel 1 (
		echo Erro: falha ao criar virtualenv. Verifique se o Python esta no PATH.
		exit /b 1
	)
	if exist "requirements.txt" (
		echo Instalando dependencias de requirements.txt...
		".venv\Scripts\pip" install --upgrade pip
		".venv\Scripts\pip" install -r requirements.txt
		if errorlevel 1 (
			echo Aviso: instalacao de dependencias falhou. Continuando sem bloquear.
		)
	) else (
		echo Nenhum requirements.txt encontrado. Pulando instalacao de dependencias.
	)
)

REM Ativa a virtualenv se estiver disponivel
if exist ".venv\Scripts\activate.bat" (
	call ".venv\Scripts\activate.bat"
) else (
	echo Aviso: ".venv\Scripts\activate.bat" nao encontrado. Continuando sem ativar venv.
)

REM Define a porta 8080 como padrao se %PORT% nao estiver definida
if "%PORT%"=="" (
	set PORT=8080
)

echo Iniciando servidor na porta %PORT%...
python -u -m flask --app app run -p %PORT% --debug