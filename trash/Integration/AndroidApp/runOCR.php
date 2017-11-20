<?php 

// echo 'HI SAM <br>';	
$command = 'python cli.py';//escapeshellcmd('cli.py');
exec($command, $out, $status);
// $out = str_replace("<!!>","<br>",$out);
// $output = shell_exec($command);
echo implode("<br>",$out);
// echo $status;

?>