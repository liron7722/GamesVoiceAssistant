function changeColor(){
     var content;
     var file = 'voice_assistant_status.txt';
     var rawFile = new XMLHttpRequest();

     rawFile.open("GET", '../../Files/voice_assistant_status.txt', false);
     rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                content = rawFile.responseText;
            }
        }
    }
    rawFile.send(null);
    if(content.includes('off'))
    {
        var elements = document.getElementsByClassName("leds")
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.background='#F00';
        }
    }
    else if(content.includes('on'))
    {
        var elements = document.getElementsByClassName("leds")
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.background='#ABFF00';
        }
    }
    else if(content.includes('record'))
    {
        var elements = document.getElementsByClassName("leds")
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.background='#ff9900';
        }
    }
    else if(content.includes('listen'))
    {
        var elements = document.getElementsByClassName("leds")
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.background='#FF0';
        }
    }
    else if(content.includes('speak'))
    {
        var elements = document.getElementsByClassName("leds")
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.background='#24E0FF';
        }
    }
};


  /*Red*/
  /*background-color: #F00;
  box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #441313 0 -1px 9px;*/

  /*Green*/
  /*background-color: #ABFF00;
  box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #304701 0 -1px 9px;*/

   /*Orange*/
  /*background-color: #ff9900;
  box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #cc6600 0 -1px 9px;*/

  /*Yellow*/
  /*background-color: #FF0;
  box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #808002 0 -1px 9px;*/

  /*Blue*/
  /*background-color: #24E0FF;
  box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #006 0 -1px 9px;*/