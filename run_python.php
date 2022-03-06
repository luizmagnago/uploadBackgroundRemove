<?php
   $filename = $_POST['filename'];
   $background_video = $_POST['background_video'];

   shell_exec("sudo chmod -R 777 .");

   $call = '/usr/bin/python2.7 generateVideo.py --input '. $filename. ' --background_video '. $background_video;

   ob_start();
   passthru($call);
   $output = ob_get_clean();

   if (strpos($output, 'ERROR') !== false) {
      echo json_encode(array("abc"=>$output));  
   }
   else {
      echo json_encode(array("abc"=>$filename));
   }

?>
