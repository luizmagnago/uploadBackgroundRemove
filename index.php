<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<meta name="description" content="Dynamic File Uploader to upload file with real time upload progress, total size of file etc.">
	<meta name="keywords" content="dynamic, uploader, upload, file, realtime, progress, procces, size, etc.">
	<meta name="author" content="Md. Saifur Rahman and Shakil Ahmed">
	<meta property="og:image" content="https://i.ibb.co/HtqRhv3/logo.png">
	<title>File Uploader</title>
	<link rel="shortcut icon" href="https://i.ibb.co/k6ZrV5t/icons8-upload-64.png" type="image/x-icon">
	<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@400;700&display=swap">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

	<link rel="stylesheet" href="style.css">
</head>
<body>

	<div class="section">
		<div class="container">
			<h1 class="title">File uploader</h1>

			<form method="POST" id="upload_form" enctype="multipart/form-data">

				<label class="title" for="city_list">Choose City Background:</label>
				<div class="title">
					<select name="city_list" id="city_list">
						<option value="aux_files/cairo1.mp4" selected>Cairo</option>
						<option value="aux_files/dubai.mp4" >Dubai</option>
						<option value="aux_files/jeddah.mp4" >Jeddah</option>
						<option value="aux_files/madina.mp4" >Madina</option>
						<option value="aux_files/riyadh.mp4" >Riyadh</option>
						<option value="aux_files/taif.mp4" >Taif</option>
					</select>
				</div>

				<br>

				<span class="label">tap the plus icon to choose file</span>
				<input type="file" accept=".jpg, .png, .jpeg, .gif, .bmp, .tif, .tiff|image/*" name="file[]" id="file" class="file" data-multiple-caption="{count} files are selected">

				<label for="file" class="file" >
					<span id="filename_" class="block white">No file is chosen</span>
					<i class="fas fa-plus-circle fa-2x"></i>
				</label>


				<!-- <img id="uploadPreview" class="preview" id="preview"> -->

				<button type="button" value="Upload" class="submit" id="submit">Upload</button>
                
				<div id="pass">
				
				</div>

				
			</form>
			
			<form method="POST" id="send_email" style="display:none;">
			<input type="email" required id="email"/> 
			<button type="button" value="Send" class="submit" id="send_email_submit">Send Email</button>
			<div id="spass">
			
				</div>
			</form>
			<div id=videoProgress class="spinner spinner-md" style="display:inline;" ></div>
		
			

			<!-- <div class="credit">
				<span>copyright &copy; 2020. all right reserved by <a href="#">Codebumble Inc.</a></span>
			</div> -->
		</div>
	</div>

	<!-- <script src="app.js"></script> -->

	<script>
	var outputfile = null;
	

		document.getElementById("videoProgress").style.display = 'none';
		document.getElementById("send_email").style.display = 'none';
		

		// Files Counter
		(function (document, window, index) {
			var inputs = document.querySelectorAll('.file');
			Array.prototype.forEach.call(inputs, function (input) {
				var label = input.nextElementSibling,
					labelVal = label.innerHTML;

				input.addEventListener('change', function (e) {
					var fileName = '';
					if (this.files && this.files.length > 1)
						fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}',
							this.files.length);
					else
						fileName = e.target.value.split('\\').pop();

					if (fileName) {
						// label.querySelector('span').innerHTML = fileName;
						document.getElementById("filename_").textContent = fileName;
					}
					else {
						document.getElementById("filename_").textContent = 'No file is chosen';
						//label.innerHTML = labelVal;
					}
				});

				// Firefox bug fix
				input.addEventListener('focus', function () {
					input.classList.add('has-focus');
				});
				input.addEventListener('blur', function () {
					input.classList.remove('has-focus');
				});
			});
		}(document, window, 0));


	// Preview

	// document.getElementById("file").addEventListener("change", function(){
	// 	var oFReader = new FileReader();
	// 	oFReader.readAsDataURL(document.getElementById("file").files[0]);

	// 	oFReader.onload = function (oFREvent) {
	// 		document.getElementById("uploadPreview").src = oFREvent.target.result;
	// 	};
	// })

	// Progress Bar
	function _(el) {
		return document.getElementById(el);
	}

	document.getElementById("submit").addEventListener("click", function () {
		$("#pass").html("");
		
        var input = document.getElementById('file');
        for (var i = 0; i < input.files.length; ++i) {
            $("#pass").append("<div class=\"progress\" id=\"progress-bar-sh-"+i+"\"><div id=\"myBar-"+i+"\" class=\"progress-bar progress-bar-striped active\" style=\"width:0%\">0%</div></div><div id=\"stats-"+i+"\" class=\"white\"><h3 id=\"status-"+i+"\"></h3><p id=\"loaded_n_total-"+i+"\"></p><p id=\"shakil-"+i+"\">Uploaded: <span id=\"n_loaded-"+i+"\"></span> / <span></span><span id=\"n_total-"+i+"\"></span><span id=\"n_per-"+i+"\"></span></p></div>");
	
            		var file = _("file").files[i];
		// alert(file.name+" | "+file.size+" | "+file.type);
		var formdata = new FormData();
		formdata.append("file", file);
		var ajax = new XMLHttpRequest();
		ajax.upload.addEventListener("progress", progressHandler.bind(null, i), false);
		ajax.addEventListener("load", completeHandler.bind(null, i), false);
		ajax.addEventListener("error", errorHandler.bind(null, i), false);
		ajax.addEventListener("abort", abortHandler.bind(null, i), false);
		ajax.open("POST", "dependency.php");
		ajax.send(formdata);
           }

	});
	
	function progressHandler(num,event) {
	    	var link = document.getElementById("status-"+num);
		var elem = document.getElementById("myBar-"+num);
		
		var percent = (event.loaded / event.total) * 100;
		var width = Math.round(percent);

		var frame = Math.round(percent);
		var id = setInterval(frame, 100);

		elem.style.width = width + '%';
		elem.innerHTML = width * 1 + '%';


		var load = (event.loaded / (1024 * 1024));
		var loaded = Math.round(load);

		var total = (event.total / (1024 * 1024));
		var totalr = Math.round(total);
		
		_("n_total-"+num).innerHTML = +totalr + " MB";
		_("n_loaded-"+num).innerHTML = +loaded + " MB";
		_("n_per-"+num).innerHTML = " (" + width + "%)";
		if(width == 100){
			elem.classList.add("progress-bar-success");
			elem.innerHTML = "Complete";
			link.classList.remove("hide");
			link.classList.add("show");
		}
	}

	document.getElementById("file").addEventListener("click",function() {
		$("#pass").html("");
		
});

	function completeHandler(num,event) {
	    $("#progress-bar-sh-"+num).css({ display: "none" });
	     $("#loaded_n_total-"+num).css({ display: "none" });
	     $("#shakil-"+num).css({ display: "none" });
		_("status-"+num).innerHTML = event.target.responseText;
		// _("progressBar").value = 0;

		var res = event.currentTarget.response;

		var mySubString = res.substring(
    		res.indexOf("'") + 1, 
    		res.lastIndexOf("'")
		);

		var select = document.getElementById('city_list');
		var background_video_name = select.options[select.selectedIndex].value;

		document.getElementById("videoProgress").style.display = 'table';

		$.ajax({
            url:"run_python.php",    //the page containing php script
            type: "post",    //request type,
            dataType: 'json',
            data: {filename: mySubString, background_video: background_video_name},
            success:function(result){

				console.log("Runned python script")

				let resIncludes = result.abc.includes("ERROR");

				if (resIncludes == true) {
					console.log("Error: ", result.abc)
					_("status-"+num).innerHTML = _("status-"+num).innerHTML + "<br/>Error on video processing!!!";
					document.getElementById("videoProgress").style.display = 'none';
				}
				else {
					let ret = result.abc;

					var filename = ret.replace(/^.*[\\\/]/, '');

					let fileNoExt = filename.split('.').slice(0, -1).join('.');


					let videoPath = "videoOut/" + fileNoExt + ".mp4"

					let videoPathOut = "videoOut/" + fileNoExt + "_.mp4"

					//
					outputfile = null;
					$.ajax({
					url:"run_ffmpeg.php",    //the page containing php script
					type: "post",    //request type,
					dataType: 'json',
					data: {filename: videoPath, filenameOut: videoPathOut},
					success:function(result){

						console.log("Running ffmpeg")

						// console.log(result)

						// console.log(videoPathOut)

						// console.log(fileNoExt)


						let ahref = "<a href='" + videoPathOut + "'>" + fileNoExt + "_.mp4" + "</a>";


						// console.log(ahref)


						_("status-"+num).innerHTML = _("status-"+num).innerHTML + "<br/>Video Download: " + ahref;

						document.getElementById("videoProgress").style.display = 'none';
						document.getElementById("send_email").style.display = 'table';
						outputfile = fileNoExt + "_.mp4";

						}
					});

					

					
				}



            }
        });
	}
	
	document.getElementById("send_email_submit").addEventListener("click", function () {	
		email = document.getElementById("email").value
		document.getElementById("videoProgress").style.display = 'table';
		$.ajax({
		    type: 'POST',
		    url: "send_email.php",
		    dataType: 'json',
		    data: {'outputfile' : outputfile, 'email' : email},
		    success: function (data) {
		    // console.log(data)
		    if (data.success) {
		    $("#spass").html("Send Succesfully");
		    } else {
		    $("#spass").html("Error while Sending Email, Please try again");
		    }
		    
		    document.getElementById("videoProgress").style.display = 'none';
		    }
		});
	});

	function errorHandler(num,event) {
	    $("#progress-bar-sh-"+num).css({ display: "none" });
	     $("#loaded_n_total-"+num).css({ display: "none" });
	     $("#shakil-"+num).css({ display: "none" });
		_("status-"+num).innerHTML = "Upload Failed";
	}

	function abortHandler(num,event) {
	    $("#progress-bar-sh-"+num).css({ display: "none" });
	     $("#loaded_n_total-"+num).css({ display: "none" });
	     $("#shakil-"+num).css({ display: "none" });
		_("status-"+num).innerHTML = "Upload Aborted";
	}
	
	</script>
	<script src="https://kit.fontawesome.com/6b46e3b6bd.js" crossorigin="anonymous"></script>
</body>
</html>
<!-- <script>
    var elem = document.getElementsByTagName("div")[6];
    elem.remove();
</script> -->
