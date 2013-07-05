/* Very basic tooltip for anchor mouseover
 *
 * Copyright stuff:
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 * 
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 * LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

$(document).ready(function() {
    //Select all anchor tag with rel set to tooltip
    $('a[rel=tooltip]').mouseover(function(e) {
        
        //Grab the title attribute's value and assign it to a variable
        var tip = $(this).attr('title');    
        
        //Remove the title attribute's to avoid the native tooltip from firefox
        $(this).attr('title','');
        
        //Append the tooltip template and its value
        $(this).append('<div id="tooltip"><div class="tipHeader"></div><div class="tipBody">' + tip + '</div><div class="tipFooter"></div></div>');        
        
        //Set the X and Y axis of the tooltip
        $('#tooltip').css('top', e.pageY + 30 );
        $('#tooltip').css('left', e.pageX - 90);
        
        //Show the tooltip with fadeIn effect
        $('#tooltip').fadeIn('500');
        $('#tooltip').fadeTo('10',0.8);
        
    }).mousemove(function(e) {
    
        //Keep changing the X and Y axis for the tooltip, thus, the tooltip move along with the mouse
        $('#tooltip').css('top', e.pageY + 30 );
        $('#tooltip').css('left', e.pageX - 90);
        
    }).mouseout(function() {
    
        //Put back the title attribute's value
        $(this).attr('title',$('.tipBody').html());
    
        //Remove the appended tooltip template
        $(this).children('div#tooltip').remove();
        
    });
});
