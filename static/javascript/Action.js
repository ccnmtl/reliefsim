/* Start
       # Author : Magic 
       # Date : 12/10/2007 
       # Description: 1. Control the client site functionality.
					  2. Send request to python controller using xml_http.
					  3. Set response of server in page.
	End.
*/
/*********************************************************************************/



var strAssigndTask = "";						// task value
var astrMemberName="" ;							// asigned Member Name
var strMemberName="";							// member Name Responce from Server	
var objFrmTask;									// object form
var objMessageContent;							// object Message Container
var objStatus;									// Object player Status
var intTurnNO=0;								// turn No

var strBtnSource;								// assignBtn image Src							
var boolBtnstatus=false;						// assignBtn status
var boolTaskStatus=false;						// Task Status
var boolShowHelp=false;							// Help tooltip status
var strPlayerStatus;							// Player Status 
var strVstatus_Player;							// player class Status 
var objTurn;									// Object Turn no in page
var objCanvas;									// Object div tag containg Canvas
var currentTask;								// current task which is assigned
var ataskAssigned=new Array();					// array of asigned member & label to change background 

var arrDataPopulation=new Array();				// Array for Total Population Data  
var arrPopulationleFive=new Array();			// Array for Total Population less then five age group Data  
var arrPopulationlbetFive=new Array();			// Array for Total Population age group between five to fourteen Data
var arrpopulationlabovefifteen=new Array();		// Array for Total Population age group above fifteen Data
var objhelpCheck;								// Object button Help on
var objinforMationWindow						// Help Information Window Object




/********************************************************************
*	 function to selectTask 
//   return @ param strAssigndTask 
//	 set message on objMessageContent
********************************************************************/

function fnselectTask ()
{

	for (var i = 0; i < objFrmTask.elements.length; i++)
	{
		if (objFrmTask.elements[i].checked)
		{
			if(objFrmTask.elements[i].type="radio")
				strAssigndTask=objFrmTask.elements[i].value;
				boolTaskStatus=true;
				if(boolTaskStatus){
				objMessageContent.style.color="#000000";
//				objMessageContent.innerHTML="Click on Assign button next to a Team Member to assign this task."
				objMessageContent.innerHTML='Message: Assign this to a member of your team by clicking the "ASSIGN" button next to their name.';
				}
		}
    }
}



/********************************************************************
*	functions  to assign task to member
//  pass Param @ obj "memberName"
//  set proper message on objStatus & objMessageContent
********************************************************************/

function fnchangeStatus(obj){
	var	objStatus=document.getElementById("status_"+ obj);
	objMessageContent.style.color="#000000";
	fnselectTask ();
	strMemberName=obj;
	if (strAssigndTask!="")
	{
		if(strPlayerStatus=="available")
		{
			fnAssignTask(strMemberName);
			strAssigndTask="";
			//fnassignedTask(strMemberName, currentTask);
			//currentTask.style.backgroundColor="#CFBA81";
			boolTaskStatus=false;
			taskturnNo="1";
		}else
		{
			strAssigndTask="";
			objMessageContent.style.color="red";
		}
	}else{
		if(!boolTaskStatus && strPlayerStatus=="available")
		{
		objMessageContent.innerHTML = "Message: Select a task to be assigned to the team member first.";
		}
		else
		{
			var resetLabel;
			resetLabel=ataskAssigned[strMemberName];
			var strresetLabel=resetLabel				// resetLabel.id;
			var k=0;
			document.getElementById(resetLabel).style.backgroundColor="";
			fnUnAssign(strMemberName);
			fnassignedTask(strMemberName, "");
			objStatus.innerHTML="available";
			boolBtnstatus=false;
			boolTaskStatus=false;
		}
	}
	objFrmTask.reset();
}


// function to add array item "member Name" & assignedTask Label
function fnassignedTask(member, taskLabel){
	ataskAssigned[member] = taskLabel;
		if (taskLabel!="")
		{
			currentTask=document.getElementById(taskLabel);
			currentTask.style.backgroundColor="#CFBA81";
		}
}



/********************************************************************
*	functions to call changeStatus
//  @ param obj "membername"
//  call fnchangeStatus(obj)
********************************************************************/
function fndoAction(obj){
		fnchangeStatus(obj);
}
/********************************************************************
*	End functions to call change status
********************************************************************/



/// Information window 
	var mblnOnInfoRaiser = false;
	var mblnOnInfoWindow = false;

/// Loading Data in Popup Window...
    var IE = document.all?true:false
	// If NS -- that is, !IE -- then set up for mouse capture
		if (!IE) document.captureEvents(Event.MOUSEOVER)
		var mintWaitForDisplay = 2000;
		var e = window.event;
		var mintPreviousTimeout = 0; 		
		var mstrInformationTargetID = '';
		var mobjEventSource;
		var mintXPos;	
		var mintYPos;


		
/********************************************************************
*	functions  to show & hide information window
********************************************************************/
		
//  function to retrieve mouse x-y pos    
		function fngetMouseXY(e) {
			// x-y pos.s if browser is IE
			if (IE) { 
				var position=getScrollingPosition();
				mintXPos = event.clientX  + position[0];
				mintYPos = event.clientY + position[1];
			} 
			else
			{  
			// x-y pos if browser is NS
			mintXPos = e.pageX;
			mintYPos = e.pageY;
			}
			if (mblnOnInfoRaiser == false && mblnOnInfoWindow == false)
			{
				var objInfoDiv = document.getElementById("divInformationWindow");
				objInfoDiv.style.display = 'none';
			}
		}
		// end //


// To fix information window position bug in Ie6 & Ie7,   
//  @ param Return x, y in array "position".
		function getScrollingPosition()
		{
			var position = [0, 0];
				if (typeof window.pageYOffset != 'undefined')
					{
					position = [
					window.pageXOffset,
					window.pageYOffset
					];
					}
				else if (typeof document.documentElement.scrollTop != 'undefined' && document.documentElement.scrollTop > 0)
					{
					position = [
					document.documentElement.scrollLeft,
					document.documentElement.scrollTop
					];
				}
				else if (typeof document.body.scrollTop != 'undefined')
				{
					position = [
					document.body.scrollLeft,
					document.body.scrollTop
					];
				}
			return position;
		}


// pass @param objSource "label Id"
// call function fnShowInformation
	function fnDisplayHelp(objSource)
		{
			mblnOnInfoRaiser = true;
			try
			{
				var strCurrentObjectID;
				if (objSource.tagName == "label")													// Get The ID Of Element For Which The Event Is Fired
				{	
					strCurrentObjectID = objSource.attributes['for'].value;	
				}
				else 
				{	strCurrentObjectID = objSource;	
				}
	
				if (mstrInformationTargetID == strCurrentObjectID)
				{	return;	}
				else
				{	
					mstrInformationTargetID = strCurrentObjectID;	
				}
	
				mobjEventSource = objSource;
				// Clear Previous Timeout If Any	
				try
				{	window.clearTimeout(mintPreviousTimeout);	}
				catch (e){alert(e.message);}
				mintPreviousTimeout = window.setTimeout(fnShowInformation, mintWaitForDisplay);		// Set New Timeout
			}
			catch (ex)
			{	alert(ex.message);	}				
		}


// show information window
		function fnShowInformation()
		{
			objInfoDiv = document.getElementById("divInformationWindow");
			if (mintYPos>=450)
			{
			objInfoDiv.style.top  = (mintYPos - 280) + "px" ;											//  fnGetAbsoluteTop(mintYPos);
			}
			else{
			objInfoDiv.style.top  = (mintYPos - 5) + "px" ;											//  fnGetAbsoluteTop(mintYPos);
			}

			objInfoDiv.style.left = (mintXPos - 5) + "px";											//  Set Display Positions;

			objInfoDiv.style.display = "block";														//  Show InfoWindow

			fncallxmlAjaxFunction();																
			//  call ajax function after set the infoWindow

			// Clean Up Settings
			mstrInformationTargetID	= '';
			window.clearTimeout(mintPreviousTimeout);
		}




/********************************************************************
*	function to hide information window
********************************************************************/

		function fnhideInformation()
		{
			mblnOnInfoWindow = false;
		}



/********************************************************************
*	Clear Display Call If Moved Out Before Display Interval
********************************************************************/
		function fnClear()
			{	
				var objInfoWindow;
				try
				{	mstrInformationTargetID	= '';
					window.clearTimeout(mintPreviousTimeout);
				}
				catch(e){alert("Error: " + e.message);}
				mblnOnInfoRaiser = false;
			}



/********************************************************************
*	call Ajax and set response of ajax request into div innerHTML
********************************************************************/
function fnRequestwinStatusChanged() 
{
	if (http_request.readyState == 4)    
	{
        if (http_request.status == 200)
		{ 
			var myText = http_request.responseText;
			var objxmlPlaceHolder=document.getElementById("textResponce");
			objxmlPlaceHolder.innerHTML = myText;						// Load Data From XML File To Content Area
		}else{
			var objxmlPlaceHolder=document.getElementById("textResponce");
			objxmlPlaceHolder.innerHTML =" Request to server is Faild..";
		}
	}                   
}



/********************************************************************
*	Send Request Using Ajax to python controller
********************************************************************/
function fncallxmlAjaxFunction()
{
        var senddata = mstrInformationTargetID;
		var url = "/loadData?senddata="+senddata;
 
     // To remove firefox bug :
        if (navigator.appName =="Netscape")
		{
			   http_request.open("GET", url, true);
		}
        else
        {
                http_request.open("GET", url, true);
        }
		http_request.onreadystatechange = fnRequestwinStatusChanged;
    http_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		http_request.send(senddata);  
}




/********************************************************************
*	function to Create object to call Ajax
********************************************************************/
function fncreatexhrObject()
{
        var http_request = false;
          try
          {
                http_request = new XMLHttpRequest();
                
          }
          catch (err1)
          {
                try
                {
                      http_request = new ActiveXObject("Msxml2.XMLHTTP");
                      
                }
                catch (err2)
                {
                        try
                        {
                               http_request = new ActiveXObject("Microsoft.XMLHTTP");
                        }
                        catch(err3)
                        {
                              http_request = false;
                        }
                }               
          }
          if (!http_request)
                {
                        alert('Cannot create XMLHTTP instance');
                        return false;
                 }
         return http_request;
}
http_request = fncreatexhrObject();
/********************************************************************
*	End Create object to call Ajax
********************************************************************/





/********************************************************************
*	Show Msg Window after every end Turn. 
********************************************************************/
var intID;
var indId1;
var browser=navigator.appName;
var b_version=navigator.appVersion;
var version=parseFloat(b_version);

function fnpopupWindow(){
windowObj=getElement("turnWindow");
objendTurnwindow=getElement("endTurnwindow");
windowObj.style.zIndex=2;
objendTurnwindow.style.zIndex=10;
// alert("windowObj-"+windowObj.style.zIndex);
//  alert("objendTurnwindow-"+objendTurnwindow.style.zIndex);
// objendTurnwindow.style.zIndex=99999;
 msgObj=getElement("msgendTurn");
 msgObj.innerHTML="Your team is busy performing the actions you assigned...";
 parentWindow=getElement("dataContainer");
 intTurnNO=parseInt(intTurnNO+1);
	Effect.fadeIn(windowObj);
	Effect.setOpacity(parentWindow, 0.2);
	if (browser=="Microsoft Internet Explorer")
	{
		intID = setTimeout(fnchangeMsg, 5500);
	}else{
		intID = setTimeout(fnchangeMsg, 3900);
	}
	
}


// Disapering the msg window 
function fndisapWindow(){
  Effect.fadeOut(windowObj);
  Effect.setOpacity(parentWindow, 1);
//  objTurn.innerHTML=intTurnNO;
//  fnresetmemberStatus();
}


// change msg in msg window
function fnchangeMsg(){
	var msgObj=getElement("msgendTurn");
	msgObj.innerHTML="Three Days  Later...";
	clearTimeout(intID);
    objMessageContent.innerHTML="";
    fnSendRequest(endTaskReq);
	indId1= setTimeout(fndisapWindow, 2000);	
	boolendTurn=false;
}

/*window.onscroll = function () {
	if (windowObj)
	{
	windowObj.style.top = document.body.scrollTop + 250;
	}
}*/
/********************************************************************
*	End Show Msg Window after every end Turn. 
********************************************************************/


function resetBackground(){
	var objLabel=fngetElementsByClass('labelText',document,'label');
	for (var counter = 0; counter < objLabel.length; counter++)
		{
			var arrLabel   = objLabel[counter];
			arrLabel.style.backgroundColor="";
		}
}



/********************************************************************
*
*	Get All Page Object According to requirement & call function according to events
*	get object objFrmTask
*   get object objLabel
*   get object objMessageContent
*	get object objTurn
*   get object objCanvas
*	get object btnEndTurn
*	get object objhelpCheck
*	get object btnCloseinformation
*	get object btnQuit
********************************************************************/
function fngetPageobject(){
	objFrmTask = getElement("frmTask");
	var objLabel=fngetElementsByClass('labelText',document,'label');
	var aPlayerNameav=fngetElementsByClass('player_Name available',document,'div');
	var aPlayerNamebus=fngetElementsByClass('player_Name busy',document,'div');
	objMessageContent=getElement("messageContent");
	objinforMationWindow=getElement("inforMationWindow");
	objTurn=getElement("turnNo");
	objCanvas=getElement("divData");
	var btnGraph=getElement("btnGraph");
	var btnEndTurn=getElement("endTurn");
	objhelpCheck=getElement("showHelp");
	var btnCloseinformation=getElement("closeBtn");
	var btnQuit=getElement("btnQuit");
	var btnClose=getElement("btnClose");
	

	// store value of current selected radio button
	for (var i = 0; i < objFrmTask.elements.length; i++)
	{
		arrradioBtn   = objFrmTask.elements[i];
		
		if (arrradioBtn.type="radio")
		{
			arrradioBtn.onclick=function()		
			{
				fnselectTask();
			}
		}
    }

// store current label on rollover
		for (var counter = 0; counter < objLabel.length; counter++)
		{
			var arrLabel   = objLabel[counter];
			arrLabel.onclick=function()
				{
					currentTask=this;
				}
				arrLabel.onmouseover=function()
				{
					var taskId=this.id;
					if(boolShowHelp)
					{
						fnDisplayHelp(taskId);
                        objinforMationWindow.style.display="none";   ///  Information Window hide on rollover new
					}
				}

				arrLabel.onmouseout=function(){
					fnClear();
				}
		}

	fnselectMember();

	btnEndTurn.onclick=function(){
		fnpopupWindow();
		fnTurnEnd(this.id);
		this.src="../static/images/btn_endTurn.gif";
	}
	
	btnEndTurn.onmouseover=function(){
		this.src="../static/images/btn_endTurn_over.gif";
	}
	
	btnEndTurn.onmouseout=function(){
		this.src="../static/images/btn_endTurn.gif";	
	}

	objhelpCheck.onclick=function(){
		fntoggleHelp();
	}
	
	objhelpCheck.onmouseover=function(){
		var btnPath=this.src;
		var arrBtnPath=btnPath.split("/");
		var btnImage=arrBtnPath.pop();
		if (btnImage=="helpbutton_On.gif")
		{
			this.src="../static/images/helpbutton_Over.gif"
		}
	}

	objhelpCheck.onmouseout=function(){
		var btnPath=this.src;
		var arrBtnPath=btnPath.split("/");
		var btnImage=arrBtnPath.pop();
		if (btnImage=="helpbutton_Over.gif")
		{
			this.src="../static/images/helpbutton_On.gif"
		}
	}

	btnCloseinformation.onclick=function(){
			objInfoDiv.style.display="";
	}
	
	btnQuit.onmouseover=function(){
			this.src="../static/images/btn_quit_over.gif"
	}		

	btnQuit.onmouseout=function(){
			this.src="../static/images/btn_quit.gif";
	}		

	btnQuit.onclick=function(){
		fnquitGame();
	}

	btnGraph.onclick=function(){
		fnshowHideGraph();
		this.src="../static/images/butt_viewchart_normal.jpg";
	}

	btnGraph.onmouseover=function(){
		this.src="../static/images/butt_viewchart_over.jpg";
	}

	btnGraph.onmouseout=function(){
		this.src="../static/images/butt_viewchart_normal.jpg";
	}

	btnClose.onclick=function (){
		fnshowHideGraph();
	}

}

/********************************************************************
*	End Get All Page Object According to requirement & events call  
*
********************************************************************/
function fnshowHideGraph(){
	var graphObj=getElement("population");
	
	if (graphObj.style.visibility!="visible")
	{
		graphObj.style.visibility="visible";
		
	}else{
		graphObj.style.visibility="hidden";
	}
}

/********************************************************************
*	Check Page is loaded Complete....
********************************************************************/
function fndoload () {
    if (document.getElementsByTagName &&
            document.getElementsByTagName ('body')) {
        //fngetPageobject();
		document.onmouseover = fngetMouseXY;
		fnSendRequest("newGame");
    }
}
/********************************************************************
*	End Check Page is loaded Complete....
********************************************************************/


window.onload = fndoload;													// Calling fndoload function 




/********************************************************************
//  function Search Class by Name 
//	return array of classEmenets
//  @ param classname , node, tagname to limit the search
********************************************************************/
function fngetElementsByClass(searchClass,node,tag) {
	var aclassElements = new Array();		
	if ( node == null )
		node = document;
	if ( tag == null )
		tag = '*';
	var els = node.getElementsByTagName(tag);
	var elsLen = els.length;
	var pattern = new RegExp("(^|\\\\s)"+searchClass+"(\\\\s|$)");
	for (i = 0, j = 0; i < elsLen; i++) {
		if ( pattern.test(els[i].className) ) {
			aclassElements[j] = els[i];
			j++;
		}
	}
	return aclassElements;
}
// Search Class by Name end





/********************************************************************
*	Select Member to assign the task
*   return @ astrMemberName
*   call fnteamStatus
********************************************************************/
function fnselectMember(){
	astrMemberName=fngetElementsByClass('btn_assign_unassign',document,'div');   
	fnteamStatus();
}
/********************************************************************
*	End Select Member to assign
********************************************************************/





/********************************************************************
*	Function to set Team Status 
*   return @ astrmemberStatus
*	return @ strPlayerStatus
*   return @ strVstatus_Player
*   return @ strBtnSource
*   call fuinction fndoAction(assignMember) // pass Param @assignMember
********************************************************************/

function fnteamStatus(){
	var astrmemberStatus=fngetElementsByClass('assign',document,'img'); 
	for (var counter = 0; counter < astrmemberStatus.length; counter++)
		{
			var arrMemberStat=astrmemberStatus[counter];
			// roolover Image src
				arrMemberStat.onmouseover=function(){
				btnPath=this.src;
				arrbtnPath=btnPath.split("/");
				btnPath=arrbtnPath.pop();
				if (btnPath!="btn_unassign.gif")
				{
					this.src="../static/images/btn_assign_over.gif";
				}

			}
			// roolout Image src
				
			arrMemberStat.onmouseout=function()
				{
					btnPath=this.src;
					arrbtnPath=btnPath.split("/");
					btnPath=arrbtnPath.pop();
					if (btnPath!="btn_unassign.gif")
					{
						this.src="../static/images/btn_assign.gif";		
					}	
				}
				
			
				arrMemberStat.onclick=function()
				{
					var btnClicked=true;
					var assignMember=this.id;
					strPlayerStatus=getElement("status_"+assignMember);
					strPlayerStatus=strPlayerStatus.innerHTML;
					strVstatus_Player=getElement("vstatus_"+assignMember);
					var strBtnSource=this.src;

					fnchangeImageStatus(strBtnSource);
						if(boolBtnstatus)
						{
							this.src="../static/images/btn_assign.gif";
							boolBtnstatus=false;
						}
						else
						{
							if(boolTaskStatus)
							{ 
							this.src="../static/images/btn_unassign.gif";
							}
						}
						fndoAction(assignMember);
				}
		}

}
/********************************************************************
*	End Function to set Team Status 
********************************************************************/




/********************************************************************
*	Function to change Image of assign/ unassign button
*   pass @ param strBtnSource
*   return boolean boolBtnstatus
********************************************************************/
function fnchangeImageStatus(strBtnSource){
	arrBtnSource=strBtnSource.split("/");
	strBtnSource=arrBtnSource.pop();
	if(strBtnSource!="btn_assign_over.gif")
	{	
		if (boolTaskStatus)
		{
			boolBtnstatus=false;
			fnError();
		}else{
		boolBtnstatus=true;
		}
	}
	else
	{
		boolBtnstatus=false;
	}
}
/********************************************************************
*	End Function to change Image of assign/ unassign button
********************************************************************/




/********************************************************************
*	Function to set tolltip visible / hide
*   return boolean value for boolShowHelp
********************************************************************/

function fntoggleHelp(){
        if(boolShowHelp)
        {
                boolShowHelp=false;
                objhelpCheck.title="Help On";
                objhelpCheck.src="../static/images/helpbutton_On.gif";
                objinforMationWindow.style.display="none";
        }
        else
        {
                boolShowHelp=true;
                objhelpCheck.title="Help Off";
                objinforMationWindow.style.display="block";
                objhelpCheck.src="../static/images/helpbutton_Off.gif";
        }
}
/********************************************************************
*	End Function to set tolltip visible / hide
********************************************************************/


/********************************************************/
function fnError(){
	objMessageContent.innerHTML="This user is already busy to perform the task.<br/>To assign the task please unassign first."
	objFrmTask.reset();
	boolTaskStatus=false;
}




/********************************************************************
*	Reset Value for the Prototype after EndTurn  in actual this will change Dynamicaly
********************************************************************/

function fnresetmemberStatus(){
	var objDws=getElement("dws");
	var objDfs=getElement("dfs");
	objFrmTask.reset();
	if (intTurnNO){
			function fngetXhr(xmlhttp) 
			{
				fndrawGraph();
				if (intTurnNO==3)
				{
				
					objDfs.value="16000k";
					objDfs.style.backgroundColor="#ef969c";
					objDfs.style.color="#000000";
					objDws.value="300k";
					objDws.style.backgroundColor="#ef969c";
					objDws.style.color="#000000";
				}else{
					objDfs.style.backgroundColor="";
					objDfs.style.color="#000000";
					objDws.style.backgroundColor="";
					objDws.style.color="#000000";

				}
			}

			function fnshowError(err) 
			{
			//	alert("An error occurred! The status was: " + err.number);
			}

			//var xhr = doSimpleXMLHttpRequest("turn.html");
			//xhr.addCallbacks(fngetXhr, fnshowError);
	}
}

/********************************************************************
*	End Reset Value for the Prototype after EndTurn  in actual this will change Dynamicaly
********************************************************************/

function xTicksval()
{
	var arrxTicks = new Array();
	currentGraphXval = new graphXObject("" , 0);						
	arrxTicks.push(currentGraphXval);
	
	for (var i = 1; i<= intTurnNO ; i++ )
	{
		currentGraphXval = new graphXObject(objSystemDate[i-1] , i);						
		arrxTicks.push(currentGraphXval);
	}
	return arrxTicks;
}

// Prototyping for the Xticks Object
// @ param name , value

function graphXObject(name, value) 
{ 
	this.label = name;
	this.v = value;
}

function setOptionValue ()
{
	options = {
   "IECanvasHTC": "scripts/plotkit/iecanvas.htc",
   "colorScheme":[Color.purpleColor(), Color.orangeColor(), Color.greenColor(), Color.blueColor()],  
   "padding": {left: 60, right: 10, top: 10, bottom: 20},
   "yAxis":[0,12000],
   "axisLabelColor":Color.blackColor(),
   "drawYAxis": true,
   "shouldFill": false,
   "axisLabelFontSize": 11,
   "axisLabelFont": "Verdana"
	};
        options.xTicks = xTicksval();    // set Xticks Value
}
	var layout;
	var plotter;
	var canvas;
	var jg;
	var strMain = 'Yes';
	var gaintHighlightedItems = new Array();
/********************************************************************
*	Function to Draw Graph
********************************************************************/
	function fndrawGraph() {
                setOptionValue();
				layout = new Layout("line", options);
//				alert("called.........fngraph............");
				var atempDataPopulation;
				var atempPopulationlefive;
				var atemparrPopulationbetFive;
				var atemparrpopulationlabovefifteen; 
				
				atempDataPopulation=arrDataPopulation;
				var populationlen = atempDataPopulation.length; 
				
				//arrPopulationleFive.push(populationlefive);
				atempPopulationlefive=arrPopulationleFive;
				
				//arrPopulationlbetFive.push(populationlbetfive);
				atemparrPopulationbetFive=arrPopulationlbetFive;
				
				//arrpopulationlabovefifteen.push(populationlabovefifteen);
				atemparrpopulationlabovefifteen=arrpopulationlabovefifteen;
				
				// Total Population 
				var tpBeforeInstruction="layout.addDataset('Totalpopulation',[";
				var tpInstruction="";
				

				// less then five population 
				var tpltfiveBeforeInstruction="layout.addDataset('Populationltfive',[";
				var tpltfiveInstruction="";
				var populationltfivelen = atempPopulationlefive.length;

 				// less then five to fourteen  population 
				var tpbftofourtBeforeInstruction="layout.addDataset('PopulationAge5to14',[";
				var tpbftofourtInstruction="";
				var populationbetFivelen = atemparrPopulationbetFive.length;
				
				// above then fifteen  population 
				var tpabfifteenBeforeInstruction="layout.addDataset('PopulationAge15plus',[";
				var tpabfifteenInstruction="";
				var populationabfifteenlen = atemparrpopulationlabovefifteen.length;


				// creating diffrent Dataset according Data 
				
				for (var i=0; i<populationlen; i++ )
					{
					tpInstruction=tpInstruction+ "["+i+", "+atempDataPopulation[i]+"]";	
					tpltfiveInstruction=tpltfiveInstruction+ "["+i+", "+atempPopulationlefive[i]+"]";	
					tpbftofourtInstruction=tpbftofourtInstruction+ "["+i+", "+atemparrPopulationbetFive[i]+"]";	
					tpabfifteenInstruction=tpabfifteenInstruction+ "["+i+", "+atemparrpopulationlabovefifteen[i]+"]";	
					if (i!=populationlen-1)
						{
						tpInstruction=tpInstruction + ",";
						tpltfiveInstruction=tpltfiveInstruction + ",";
						tpbftofourtInstruction=tpbftofourtInstruction + ",";
						tpabfifteenInstruction=tpabfifteenInstruction + ",";
						}
					
					}

					tpInstruction=tpBeforeInstruction+tpInstruction +"])";
					tpltfiveInstruction=tpltfiveBeforeInstruction+tpltfiveInstruction+"])";
					tpbftofourtInstruction=tpbftofourtBeforeInstruction+tpbftofourtInstruction+"])";
					tpabfifteenInstruction=tpabfifteenBeforeInstruction+tpabfifteenInstruction+"])";
					eval(tpInstruction);
					eval(tpltfiveInstruction);
					eval(tpbftofourtInstruction);
					eval(tpabfifteenInstruction);
				
				layout.evaluate();
					
				var strTemp='';
				canvas = MochiKit.DOM.getElement("graph");
				plotter = new PlotKit.SweetCanvasRenderer(canvas, layout, options);
				plotter.render();
		}



/********************************************************************
*	Function to Quit Game
********************************************************************/
function fnquitGame()
		{
			objfrmEndTurn=document.getElementById("quitForm");
			objfrmEndTurn.action="/quit" ;
			objfrmEndTurn.method="get";
			objfrmEndTurn.submit();
		}
/********************************************************************
*	End Function to Quit Game
********************************************************************/
