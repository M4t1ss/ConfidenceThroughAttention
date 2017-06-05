<?php

//Input parameters
$ref 				= $argv[1];	//path to source sentence file
$human_file 		= $argv[2];	//path to file with sentence IDs

//Open files
$inRef = fopen($ref, "r") or die("Can't open input file!");
$outRef = fopen($human_file.".human.ref", "a") or die("Can't create output file!");

$LineNumbers = file($human_file);
$lineNumberArray = array();
foreach($LineNumbers as $LineNumber) {
	$lineNumberParts = explode("\t",$LineNumber);
    $lineNumberArray[$lineNumberParts[0]] = trim($lineNumberParts[1]);
}

$i = 1;
while (($refSentence = fgets($inRef)) !== false) {
	if (array_key_exists($i, $lineNumberArray)) {
		fwrite($outRef, $refSentence);
	}
    $i++;
}