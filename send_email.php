<?php
//Import PHPMailer classes into the global namespace
//These must be at the top of your script, not inside a function
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

//Load Composer's autoloader
require 'vendor/autoload.php';

//Create an instance; passing `true` enables exceptions
$mail = new PHPMailer(true);

try {
    $file = $_POST['outputfile'];
    $email = $_POST['email'];
    //Server settings
    $mail->SMTPDebug = false;                      //Enable verbose debug output
    $mail->isSMTP();                                            //Send using SMTP
    $mail->Host       = 'smtp.mailgun.org';                     //Set the SMTP server to send through
    $mail->SMTPAuth   = true;                                   //Enable SMTP authentication
    $mail->Username   = 'postmaster@photobooth.appzy.info';                     //SMTP username
    $mail->Password   = '005c53d6215bc37112fb9ab461252e40-b2f5ed24-3a3091e5';                               //SMTP password
    $mail->SMTPSecure = 'tls';            //Enable implicit TLS encryption
    $mail->Port       = 587;                                    //TCP port to connect to; use 587 if you have set `SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS`

    //Recipients
    $mail->setFrom('photobooth@appzy.info', 'photobooth');
    $mail->addAddress($email);  
    $mail->addReplyTo('photobooth@appzy.info', 'photobooth');

    //Attachments
    //$mail->addAttachment('/home/mahmoud/laravel/MOE/uploadBackgroundRemove/videoOut/'.$file);  

    //Content
    $mail->isHTML(true);                                  //Set email format to HTML
    $mail->Subject = 'Flyadeal';
    $mail->Body    = '<a href="http://143.198.167.138/videoOut/'.$file.'" ><img src="http://143.198.167.138/aux_files/email.png"></a>';

    $mail->send();
    echo json_encode(['success' => true]);
} catch (Exception $e) {
    echo json_encode(['success' => false]);
} 
