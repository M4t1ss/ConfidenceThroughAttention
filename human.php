<?php

//Input parameters
$nematus_file 		= $argv[1];	//path to source sentence file
$neuralmonkey_file	= $argv[2];	//path to target sentence file
$human_file 		= $argv[3];	//path to file with sentence IDs

//Open files
$inNEM = fopen($nematus_file, "r") or die("Can't open input file!");
$inNM = fopen($neuralmonkey_file, "r") or die("Can't open input file!");

$outHUM = fopen($human_file.".human", "a") or die("Can't create output file!");

$LineNumbers = file($human_file);
$lineNumberArray = array();
foreach($LineNumbers as $LineNumber) {
	$lineNumberParts = explode("\t",$LineNumber);
    $lineNumberArray[$lineNumberParts[0]] = trim($lineNumberParts[1]);
}



$i = 1;
while (($nemSentence = fgets($inNEM)) !== false && ($nmSentence = fgets($inNM)) !== false) {
	if (array_key_exists($i, $lineNumberArray)) {
		if($lineNumberArray[$i] == "Nematus"){
			fwrite($outHUM, $nemSentence);
		}elseif($lineNumberArray[$i] == "Neural Monkey"){
			fwrite($outHUM, $nmSentence);
		}
	}
    $i++;
}