<?php
$list = shell_exec("ls ../lists");
$lists = preg_split('/[\r\n]+/', $list, -1, PREG_SPLIT_NO_EMPTY)
?>

<html>
	<body>
		<h1> 
			All lists
		</h1>
		<ul>
			<?php
				foreach ($lists as $entry){
					echo '<li><a href="/' . $entry . '">' . $entry . '</a></li>';
				}
			?>
		</ul>
	</body>
<html>
