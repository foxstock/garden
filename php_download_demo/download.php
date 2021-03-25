<?php
/*下載到期日 */
$expDateStr='2021-03-11 15:00:00';
/* 真正的檔案路徑 */
$source_file_url="V50_MIN5_TDY.zip";
/* 檔案顯示資訊 */
$source_file_display_name="台當月歷史五分鐘線DATA";
/* 實際儲存檔名 */
$save_file_name="FOXTDYM5".date("YmdHis").".zip";

if(date("Y-m-d H:i:s").''<$expDateStr){
	if(isset($_POST['MM_action'])&&$_POST['MM_action']=='download'&&$_POST['bookNo']!=='尚未選定'){
	header('Content-type: application/zip');
	header('Content-Disposition: attachment; filename="'.$save_file_name.'"');
	readfile($source_file_url);
	}
?>
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0,padding:0;}
html{font-size:1.5em;}
body{background:#eee;}
form,select,input{font-size:1em;height:1.5em;}
select,input{background:#ffa;border:solid 0.1em #000;}
input{background:#ff0;padding:0.5em;height:3em;}
p{background:#f00;line-height:3em;padding:0.2em;text-align:center;}
.redTxt{color:#f00;}
.smallTxt{font-size:0.8em;}
</style>
</head>
<body>
<form name="form1" action="" method="post">
<h1>測試下載數據檔案</h1>
<h3>數據檔案: <?php echo $source_file_display_name;?>.zip <span class="redTxt smallTxt">請使用PC下載</span></h3>
<input type="button" value="點我下載<?php echo $source_file_display_name; ?> Zip檔" onclick="checkForm();"/>
<input type="hidden" name="MM_action" value="download" />
<span class="redTxt">下載截止日: <?php echo $expDateStr;?>前</span>

<p>本頁面內容僅作為程式功能測試，下載內容請於24小時內自行刪除。</p>
</form>
<script>
function checkForm(){
	if(confirm('確定要下載: <?php echo $source_file_display_name;?>.zip 嗎?')){
		document.form1.submit();
	}
}
</script>
</body>
</html>
<?php }else{ ?>
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0,padding:0;}
html{font-size:2em;}
body{background:#eee;}
</style>
</head>
<body>
	<h1>下載測試結束了...Bye!</h1>
</body>
</html>
<?php } ?>