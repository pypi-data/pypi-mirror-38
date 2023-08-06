
def get_dir_hash(directory, verbose=0):
  print("directory", directory)
  digest = hashlib.sha1()

  for root, dirs, files in os.walk(path):
      for names in files:
          file_path = os.path.join(root, names)

          # Hash the path and add to the digest to account for empty files/directories
          digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())

          # Per @pt12lol - if the goal is uniqueness over repeatability, this is an alternative method using 'hash'
          # digest.update(str(hash(file_path[len(path):])).encode())

          if os.path.isfile(file_path):
              with open(file_path, 'rb') as f_obj:
                  while True:
                      buf = f_obj.read(1024 * 1024)
                      if not buf:
                          break
                      digest.update(buf)

  return digest.hexdigest()