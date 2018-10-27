# perl <script> < [whatsapp chat export] > [output csv]

%contributors = ();
%contributortext = ();
$contributor = '';

while (<>) {
	$strint = $_;
		
	next if /‎This message was deleted/;
	next if /‎image omitted/;
	next if /‎video omitted/;
	
	if ($strint =~ /^\[\d\d\/[^\]]*]([^:]*):(.*)/) 
	{
		$contributor = $1;
		$contributor =~ tr/A-Za-z0-9//cd;
		
		if (exists $contributors{$contributor}) 
		{
			$contributors{$contributor}++;
			$contributortext{$contributor} += length $2;
		} 
		else 
		{
			$contributors{$contributor} = 1;
			$contributortext{$contributor} = length $2;
		}
	} 
	else 
	{
		$contributortext{$contributor} += length $strint;
	}
}

print "Name,Messages,Characters,timewriting,timereading\n"; 

foreach (keys%contributors)
{
	$contributor = $_;
	$messagecount = $contributors{$contributor};
	$messagesize = $contributortext{$contributor};
	$minutes = $messagesize * 1.0 / 45;
	
	$minutes = sprintf("%.1f", $minutes);
	
	$minutes_read = $messagesize * 200 * 1.0 / (250*6);
	$minutes_read = sprintf("%.1f", $minutes_read);
	
	print "$contributor,$messagecount,$messagesize,$minutes,$minutes_read\n"; 

}
