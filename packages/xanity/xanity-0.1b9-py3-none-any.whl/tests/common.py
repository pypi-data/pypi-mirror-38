## pytest config
import difflib

def ls_skel_diff(path):
	tree1 = subprocess.check_output('bash ls -alh ../../xanity/skeleton')
	tree2 = subprocess.check_output(path)
	diff = difflib.ndiff(tree1,tree2)
	return ''.join(difflib.restore(diff,1))

