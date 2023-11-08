from pylint import run_pyreverse as pyreverse
args = [
  '--colorized' , 
  '--all-ancestors', 
  '--all-associated',
  '--module-names=y',
  '--output=html',
  '--output-directory=diagrams\\',
  '--project=Levus',
  '--verbose',
  'src\\'
  ]
pyreverse(argv=args)