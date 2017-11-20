<?php
$target_dir = "pic/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
// echo "$target_file";
$uploadOk = 1;
$imageFileType = pathinfo($target_file,PATHINFO_EXTENSION);
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        // echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}
// Check if file already exists
if (file_exists($target_file)) {
	unlink($target_file);
    // echo "Sorry, file already exists.";
    // $uploadOk = 0;
}
// Check file size
// if ($_FILES["fileToUpload"]["size"] > 500000) {
//     echo "Sorry, your file is too large.";
//     $uploadOk = 0;
// }
// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        // echo "<br>The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}

$command = 'python cli.py '.'http://172.25.14.229/htdocs/AndroidApp/'.$target_file;//escapeshellcmd('cli.py');
// 
// $command = 'python cli.py '.'http://10.42.0.188/htdocs/AndroidApp/'.$target_file;//escapeshellcmd('cli.py');
exec($command, $out, $status);
// $out = str_replace("<!!>","<br>",$out);
// $output = shell_exec($command);
echo "<br>The image is <br>";
echo '<img src = "'.'http://172.25.14.229/htdocs/AndroidApp/'.$target_file.'" height="400" width="340">';
// echo '<img src = "'.'http://10.42.0.188/htdocs/AndroidApp/'.$target_file.'" height="400" width="340">';
echo "<br>";
echo "<br> The text in image is<br>";
echo implode("<br>",$out);

?>