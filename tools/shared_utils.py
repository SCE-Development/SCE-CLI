import subprocess

def check_docker_status():
  try:
    subprocess.run(
      ['docker', 'ps'],
      check=True,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL
    )
    return { 
      'is_installed': True,
      'is_running': True
    }
  except FileNotFoundError:
    return { 
      'is_installed': False,
      'is_running': False
    }
  except subprocess.CalledProcessError:
    return {
      'is_installed': True,
      'is_running': False
    }