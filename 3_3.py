< ?php
$filename = 'code.bin';
$fileDecode = 'decode.gif';
$fileByte = 0;
$image = 0;
if (isset($_FILES['coder'])) {
echo '<h1>Сжатие методом LZW</h1>';
$file  = $_FILES['coder'];
readImage($file);
LZW( $image);
echo '<br><br><button><a href="'.$filename.'" download>Скачать файл</button>';
echo '<br><br><button><a href="index.html">Вернуться обратно</button>';
} else if (isset($_FILES['decoder'])) {
echo '<h1>Декомпрессия методом LZW</h1>';
$file  = $_FILES['decoder'];
readTxt($file);
unLZW( $image);
echo '<br><br><button><a href="'.$fileDecode.'" download>Скачать файл</button>';
echo '<br><br><button><a href="index.html">Вернуться обратно</button>';
} else {
echo 'Я не смог';
}
$name = '';
$format = '';

function
readImage($file){
global $format,$name,$fileByte,$image;
$limitBytes = 8;
$limitFormat = 1;
$limitSize = 10;
$fileByte =$file['size'];
echo
'Загружен файл с именем "'. $file['name'].
'" и размером '. $fileByte.
' байт';
$filePath = $file['tmp_name'];
$image = getimagesize($filePath);
echo
'<br>';
if ($image['bits'] > $limitBytes)
die('Глубина цвета не должена превышать '.$limitBytes.
' байт.');
if ($image[2] != $limitFormat)
die('Тип файла только GIF');
if ($image[1] > $limitSize | | $image[0] > $limitSize)
die('Высота и ширина изображения не должна превышать '.$limitSize.' точек.');
$name = 'tmp';
$format = image_type_to_extension($image[2]);
$path= __DIR__.'\\'.$name.$format;
if (!move_uploaded_file($filePath, $path)) {
die('При записи изображения на диск произошла ошибка.');
}
$image = imageCreateFromGif($path);
}
function
readTxt($file){
global $fileByte,$filename;
$fileByte =$file['size'];
echo
'Загружен файл с именем "'. $file['name'].
'" и размером '. $fileByte.
' байт';
$filePath = $file['tmp_name'];
if (!move_uploaded_file($filePath, $filename)) {
    die('При записи на диск произошла ошибка.');
}
}

function
LZW($im){
global $format,$name,$fileByte,$filename;
echo
'<br>';
$tr1 = "";
$tr2 = "";
$tr3 = "";
$table = array(
    0 = > 0,
          1 = > 1,
                2 = > 2,
                      3 = > 3,
                            4 = > 4,
                                  5 = > 5,
                                        6 = > 6,
                                              7 = > 7
);
$tmp = array();
for ($i=0; $i < imagesy($im);$i += 1){
for ($n=0; $n < imagesx($im);$n += 1){
$rgb = imagecolorat($im, $n, $i);
array_push($tmp, $rgb);
$tr1=$tr1.$rgb.' ';
}
}

$out="";
$arrOut=array();
$str = $tmp[0]; // строка для очередного символа из файла
// цикл:
    for
    ($i=1;$i < imagesy($im) * imagesx($im);$i += 1){
$simbol = $tmp[$i]; // Очередной
символ
из
файла =
$k =$str.$simbol;
if (array_key_exists($k, $table)){
$str =$k;
} else {
$out =$out.$table[$str].' ';
array_push($arrOut, decbin($table[$str]));
if (count($table) + 1 < 32)
$table[$k]=count($table)+1;
$str=$simbol;
}
if ($i+1 >= imagesy($im) * imagesx($im)){
array_push($arrOut, decbin($table[$str]));
$out=$out.$table[$str].' ';
}
}
foreach($table as $myarr= > $code)
{
$tr2= $tr2.$myarr.' - '.$code.'<hr>';
}
foreach($arrOut as $myarr)
{
$tr3= $tr3.$myarr.' ';
}


$data = '';
for ( $i = 0; $i < count($arrOut); $i++ ) {
$data.= pack( "n", $arrOut[$i]);
}
$bytesCount = file_put_contents( $filename, $data);

$td='<td align="center">
< div style="
width: 250
px;
height: 300
px;
overflow: auto;
">';
$tdEnd = '</div></td>';
echo
'<table border="1" cellpadding="5">
< tr >
< th > Изображение < / th >
                       < th > Исходные
данные < / th >
           < th > Таблица < / th >
                              < th > Выходные
данные < / th >
           < th > Cгенерированный
код < / th >
        < / tr >
            < tr
style = "border: 1px solid black;" > '
    .$td.
'<img src="'.$name. $format.
'" style="width:200px; image-rendering: optimizeSpeed;" >'.$tdEnd.
$td.$tr1.$tdEnd.
$td.$tr2.$tdEnd.
$td.$out.$tdEnd.
$td.$tr3.$tdEnd.
'</tr>
< / table > ';

echo
'<br Полученный файл >'.$bytesCount.
' байт, а было '.$fileByte.
'байт';
echo
'<br> Степень сжатия '.(100 -$bytesCount * 100 /$fileByte).'%'.
', информация в двоичном представлении';

}

function
ost($num){
$i = 2;
while (true & & $i < 100){
if ($num % $i == 0)
return $i;
$i + +;
}
}

function
unLZW($im){
global $fileByte,$filename,$fileDecode;
echo
'<br>';
$tr1 = "";
$tr2 = "";
$table = array(
0 = > 0,
1 = > 1,
2 = > 2,
3 = > 3,
4 = > 4,
5 = > 5,
6 = > 6,
7 = > 7
);
$data = file_get_contents($filename);
$arr = unpack('n*', $data );
$tmp = array();
foreach($arr as $myarr)
{
array_push($tmp, bindec($myarr));
$tr1 = $tr1.bindec($myarr).' ';
}


$out = "";
$str = $tmp[0];
$out. =$str;
$entry = "";
for ($i=1;$i < count($tmp);$i += 1){
$k = $tmp[$i];
if (array_key_exists($k, $table)){// array_key_exists(array_search
$entry=$table[$k];
} else if ($k == count($table)+1){
$entry =$str.','.(explode(",", $str)[0]);
} else {
$out= 'ошибка декомпресии';
break;
}
$out. = ','.$entry;
if (count($table) + 1 < 32)
$table[count($table)+1]=$str.
','.(explode(",", $entry)[0]);
$str =$entry;
}

foreach($table as $myarr = > $code)
{
$tr2 = $tr2.$myarr.
' - '.$code.
'<hr>';
}
$arrOut = explode(",", $out);
$out = "";
foreach($arrOut as $myarr)
{
$out = $out.$myarr.
' ';
}

$w = W(count($arrOut));
$img = imagecreatetruecolor(count($arrOut) / $w,$w);
$index = 0;
$colors = array(
    '0' = > imagecolorallocate($img, 255, 255, 255),
'1' = > imagecolorallocate($img, 255, 255, 0),
'2' = > imagecolorallocate($img, 255, 0, 255),
'3' = > imagecolorallocate($img, 255, 0, 0),
'4' = > imagecolorallocate($img, 0, 255, 255),
'5' = > imagecolorallocate($img, 0, 255, 0),
'6' = > imagecolorallocate($img, 0, 0, 255),
'7' = > imagecolorallocate($img, 0, 0, 0)
);
for ($x=0;$x < count($arrOut) /$w;$x++){

for ($y=0;$y < $w;$y++){
$color = $colors[$arrOut[$index]];
imagesetpixel($img, $y, $x, $color);
$index + +;
}
}
$bytesCount = imagegif($img, $fileDecode);

$td = '<td align="center">
      < div
style = "
width: 250
px;
height: 300
px;
overflow: auto;
">';
$tdEnd = '</div></td>';
echo
'<table border="1" cellpadding="5">
< tr >
< th > Исходные
данные < / th >
           < th > Таблица < / th >
                              < th > Выходные
данные < / th >
           < th > Cгенерированное
изображение < / th >
                < / tr >
                    < tr
style = "border: 1px solid black;" > '
    .$td.$tr1.$tdEnd.
$td.$tr2.$tdEnd.
$td.$out.$tdEnd.
$td.
'<img src="'.$fileDecode.
'" style="width:200px; image-rendering: optimizeSpeed;" >'.$tdEnd.
'</tr>
< / table > ';
}

function
W($num){
return intval(sqrt($num));
}

? >

