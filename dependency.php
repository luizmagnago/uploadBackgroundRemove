<?php
   if(isset($_FILES['file'])){
      $errors= array();
      $file_name = $_FILES['file']['name'];
      $file_size =$_FILES['file']['size'];
      $file_tmp =$_FILES['file']['tmp_name'];
      $file_type=$_FILES['file']['type'];
      $file_path = "uploads/".$file_name;
      $dir_path = "uploads";
   
      
      $extensions= array("html","php","js","jpeg","jpg","png","webp","gif");
      
     
      if($file_size < 1){
         $errors ='Something went wrong! Please try another file.';
      }
      
      if(empty($errors)==true){
         if(!file_exists($dir_path)){
            mkdir($dir_path, 0777, true);
            if(file_exists($dir_path) && !file_exists($file_path)){

               if(move_uploaded_file($file_tmp,"uploads/".$file_name)){
                  echo "File : <a href='uploads/$file_name'>$file_name</a>";

                  // $call = '/usr/bin/python2.7 test.py --input uploads/'. $file_name;

                  // echo "\nProcessing files - Generating mp4";

                  // ob_start();
                  // passthru($call);
                  // $output = ob_get_clean(); 

                  // echo "TTTTT : <a href='uploads/$file_name'>$file_name</a>";
                  // echo $output;
               }else{
                  echo $errors;
               }
            
            }else{
               echo $errors;
            }
         }else{
            move_uploaded_file($file_tmp,"uploads/".$file_name);
            echo "File : <a href='uploads/$file_name'>$file_name</a>";

            // $call = '/usr/bin/python2.7 test.py --input uploads/'. $file_name;

            // echo "\nProcessing files - Generating mp4";

            // ob_start();
            // passthru($call);
            // $output = ob_get_clean(); 

            // echo "TTTTT2 : <a href='uploads/$file_name'>$file_name</a>";
            // echo $output;
         }
      }else{
         print_r($errors);
      }
   }
?>
