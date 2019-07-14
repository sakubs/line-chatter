
<!DOCTYPE html>
<html>
<body>

<form action="upload.php" method="post" enctype="multipart/form-data">
    Name: <input type="text" name="name"><br>
    
    Select Line image to upload:
    <input type="file" name="fileToUpload1" id="fileToUpload1">
    <input type="submit" value="Upload Image" name="submit">
    
    Select the script text file:
    <input type="file" name="fileToUpload2" id="fileToUpload2">
    <input type="submit" value="Upload Text File" name="submit">
</form>

</body>
</html>
