<?php
   $filename = $_POST['filename'];
   $filenameOut = $_POST['filenameOut'];


   shell_exec("sudo chmod -R 777 .");

   $call = '/usr/bin/ffmpeg -i ' . $filename . ' -c:v libx264 -crf 6 -preset veryfast -c:a copy ' .$filenameOut . ' -y';

   ob_start();
   passthru($call);
   $output = ob_get_clean();


   echo json_encode(array("abc"=>$filenameOut));

?>
