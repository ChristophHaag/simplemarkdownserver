<!DOCTYPE html>
<html>
%if defined('date'):
<title>{{title}} ({{date}})</title>
% else:
<title>{{title}}</title>
%end

<xmp theme="united" style="display:none;">
{{content}}


[Home](/)
</xmp>

<script src="http://strapdownjs.com/v/0.2/strapdown.js"></script>
</html>