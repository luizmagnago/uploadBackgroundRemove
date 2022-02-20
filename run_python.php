<?php
   $filename = $_POST['filename'];

   $call = '/usr/bin/python2.7 generateVideo.py --input '. $filename;

   ob_start();
   passthru($call);
   $output = ob_get_clean();

   if (strpos($output, 'ERROR') !== false) {
      echo json_encode(array("abc"=>"ERROR"));  
   }
   else {
      echo json_encode(array("abc"=>$filename));
   }

?>
