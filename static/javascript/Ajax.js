var totalPopulation = "0";         // total population for graph
var populationlefive = "0";		// population data less then five
var populationlbetfive = "0";		// population between five to fourteen 
var populationlabovefifteen = "0";	// population above fefteen
var crtotalPopulation = "0";         // total population for graph
var crpopulationlefive = "0";		// population data less then five
var crpopulationlbetfive = "0";		// population between five to fourteen 
var crpopulationlabovefifteen = "0";	// population above fefteen
var assignObj="";				// assigned member
var strInput="";				// input string 
var unassignMember="";			// unassigned Member
var heighlitedItem = "";				// Heighlighted Turn 
var objInfoVal;					// Height light object of information gauges on change of value
var assignedMember="";			// Assigned Member
var boolendTurn=false;
var endTaskReq;

function fnSetStatus(statusResp)
{
	var responseValue = "" ;
	var html="";
	var htmlId="";
	var className="";
	var statusMessage="";
	var btnSrc="btn_assign.gif";
	var taskId="";
	arrResponse = statusResp.split("@@");
	respLength = arrResponse.length -1 ;
	for (var initilize = 0 ; initilize < respLength ; initilize++)
	{
	    responseValue += arrResponse[initilize] + "<br/>";
	}
	aresponseData=responseValue.split("<br/>");
	var btnId=0;
	for (j=0; j<aresponseData.length-1 ; j++)
	{
		afilterData=aresponseData[j].split(":");
		var playerName=afilterData[0];
		statusMessage=afilterData[1];
		var taskVal=afilterData[2];

		switch (taskVal)
		{
		case "aw" :
		taskId="ass1";
		break;
		case "aq" :
		taskId="ass2";
		break;
		case "af" :
		taskId="ass3";
		break;
		case "as" :
		taskId="ass4";
		break;
		case "ap" :
		taskId="ass5";
		break;
		case "ad" :
		taskId="ass6";
		break;
		case "adf" :
		taskId="ass7";
		break;
		case "adc" :
		taskId="ass8";
		break;
		case "add" :
		taskId="ass9";
		break;
		case "ada" :
		taskId="ass10";
		break;
		case "adm" :
		taskId="ass11";
		break;
		case "ade" :
		taskId="ass12";
		break;
		case "iw" :
		taskId="intervention1";
		break;
		case "iq" :
		taskId="intervention2";
		break;
		case "ic" :
		taskId="intervention3";
		break;
		case "id" :
		taskId="intervention4";
		break;
		case "if" :
		taskId="intervention5";
		break;
		case "itc" :
		taskId="intervention6";
		break;
		case "ita" :
		taskId="intervention7";
		break;
		case "itm" :
		taskId="intervention8";
		break;
		case "ite" :
		taskId="intervention9";
		break;
		case "itf" :
		taskId="intervention10";
		break;
		case "ivc" :
		taskId="intervention11";
		break;
		case "ivm" :
		taskId="intervention12";
		break;
		case "ive" :
		taskId="intervention13";
		break;
		}

		var	objStatus=document.getElementById("status_"+ strMemberName);
		
		if (playerName=="Ryan")
		{
			htmlId="member1";
		}else if (playerName=="Juan")
		{
			htmlId="member2";

		}else if (playerName=="Alexis")
		{
			htmlId="member3";

		}else if (playerName=="Eric")
		{
			htmlId="member4";

		}else if (playerName=="Marilyn")
		{
			htmlId="member5";

		}
		
		
		if (statusMessage!="available")
		{
			className="player_Name busy";
			btnSrc="btn_unassign.gif";
		}else{
			className="player_Name available";
			btnSrc="btn_assign.gif";
		}
		fnassignedTask(btnId, taskId);
		html=html+fncreateHtml(playerName, statusMessage, className, htmlId, btnSrc, btnId);
		btnId ++; 
	}
	var objTeam=getElement("teamPanel");
	objTeam.innerHTML=html;
	fngetPageobject();

}

/* fncreateHtml  
// @ param playerName, statusMessage, className, htmlId, btnSrc
// return htmlCode
// generate HTML For the team Section
*/
function fncreateHtml(playerName, statusMessage, className, htmlId, btnSrc, btnId){
	var htmlCode="";
	htmlCode+='<div class="player_Icon" id="' + htmlId + '"></div>';
	htmlCode+='<div class="' + className +'" id="vstatus_' + btnId +'">' + playerName + '</div>';
	htmlCode+='<div class="status" id="status_'+ btnId +'">'+ statusMessage + '</div>';
	htmlCode+='<div class="btn_assign_unassign" ><img src="../static/images/' + btnSrc + '" width="66" id="' + btnId + '" class="assign" height="19" border="0" alt="Assign/Unassign" title="Assign/Unassign" /></div>'
	return htmlCode;
}



/* To Set Messages  
// @ param msgResponse
// set message on message window.
*/
function fnSetMsg(msgResponse)
{
	var message = "";
	message = msgResponse ;
	var messageText = "Message: Have your team perform their assigned tasks by clicking \"END TURN\", or change their assignments by clicking the \"UNASSIGN\" button next to a team member, and assigning them a new task." ;
	
	if (strInput!="" && strMemberName!=""){
		var displayMessage = "Message: Task has been successfully assigned to " ;
		if(message.indexOf("false") != -1)
		{
			objMessageContent.innerHTML = messageText ;
		}
		else
		objMessageContent.innerHTML = displayMessage + assignedMember + ".";
		strInput="";
		strMemberName="";
	}else if (unassignMember!="" && !boolendTurn)
	{
	    objMessageContent.innerHTML = "Message: Task was successfully un-assigned from " + unassignMember + ".";
	}
	else if(message.indexOf("false") != -1)
	{
		objMessageContent.innerHTML = "Message:";
	}
	else
	{
		objMessageContent.innerHTML = msgResponse;
	}
}




/* To Set AgebrakDown Data data
// @ param ageBreakResp
// Set responce of server in agebreak Section
// store recent data to populate the graph
*/
function fnSetAgeBreak(ageBreakResp)
{
	var arrAgeBreak = ageBreakResp.split("$$");
	var ageBreakLength = arrAgeBreak.length -1;
	var populationData=arrAgeBreak[0];
	var agraphData=populationData.split("@@");

	for (i=0; i<agraphData.length-1 ; i++ )
	{
		var dataPopulation=agraphData[0];
		if (agraphData[1]!="?")
			{
				crpopulationlefive=agraphData[1];
			}
		if (agraphData[2]!="?")
			{
				crpopulationlbetfive=agraphData[2];
			}
		if (agraphData[3]!="?")
			{
				crpopulationlabovefifteen=agraphData[3];
			}
	}
	
	var atotalPopulation=dataPopulation.split("::");
		if (atotalPopulation[1]!="?")
		{
			crtotalPopulation=atotalPopulation[1];
		}

	for (initlize = 0 ; initlize < ageBreakLength  ; initlize++) // 8 times
	{
		var arrAgeBreakData = arrAgeBreak[initlize].split("::");
		var arrAgeSlabeData = arrAgeBreakData[1].split("@@");

		for(initili = 0 ; initili < arrAgeSlabeData.length ; initili++)
		  {
		   	objAgeBrk = document.getElementById(arrAgeBreakData[0]+"_"+initili);
			objAgeBrk.value = arrAgeSlabeData[initili];
		  }
     }
}



/* To Set Information Gauges data
// @ param infoResponse
// Set responce of server in information Gauges Section
*/
function fnSetInfoGauge(infoResponse)
{
	var arrInfo = infoResponse.split("$$");
	var arrInfoLength = arrInfo.length ;
	for (init = 0 ; init < arrInfoLength  ; init++)
	{
		arrInfoData = arrInfo[init].split("::");
		objInfo = document.getElementById(arrInfoData[0]);
		objInfoVal= objInfo.value;
		if (intTurnNO>1)
		{
			if (arrInfoData[1]!="?")
			{
				if (objInfoVal!=arrInfoData[1])
				{
				objInfo.style.backgroundColor="#ef969c";
				}else{
				objInfo.style.backgroundColor="";
				}
			}
		}

		objInfo.value = arrInfoData[1];
    	
		
	}
}



/* To set turn number 
// @ param turnResponse
// Set responce of server in turn No Section
*/
function fnSetTurnNo(turnResponse)
{
	intTurnNO=turnResponse;
	objTurn.innerHTML = turnResponse;
}




/* To get the Response from Server 
# call function
# fnSetAgeBreak(arrPageInfo[0])
# fnSetStatus(arrPageInfo[1])
# fnSetMsg(arrPageInfo[2])
# fnSetInfoGauge(arrPageInfo[3])
# fnSetTurnNo(arrPageInfo[4])
*/

function fnRequestStatusChanged()
{
	
    if (http_request.readyState == 4)
    {
        {
            if (http_request.status == 200)
            {	
             responseInfo = http_request.responseText;
		     arrPageInfo = responseInfo.split("##");
		     fnSetAgeBreak(arrPageInfo[0]);
		     fnSetStatus(arrPageInfo[1]);
		     fnSetMsg(arrPageInfo[2]);
		     fnSetInfoGauge(arrPageInfo[3]);
		     fnSetTurnNo(arrPageInfo[4]) ;
		     fnGetGraphData(arrPageInfo[5]);
		     fnGetSystemDate(arrPageInfo[7]);
		     fnSetSystemDate(arrPageInfo[6]);
            }
        }                   
    }
}
/** To get the highlighted date from server . */

function fnGetSystemDate(objDate)
{
	gaintHighlightedItems = new Array();
	var arrSystemDate = objDate.split("$$");
	for(var i = 0 ; i < arrSystemDate.length ; i++)
	{
		gaintHighlightedItems.push(arrSystemDate[i]);
	}
}


/** To Get the system date .*/

var objSystemDate = new Array();
function fnSetSystemDate(objDate)
{
	var intWidth;
	objSystemDate = new Array();
	var arrSystemDate = objDate.split("$$");
	for(var i = 0 ; i < arrSystemDate.length ; i++  )
	{
		objSystemDate.push(arrSystemDate[i]) ;
	}
	
	 objCanvas.innerHTML="";
	
	 if (objSystemDate.length < 11)
	 {
	  intWidth = 650;
	 }
	 else
	 {
	  intWidth = 650 + ((objSystemDate.length - 10) * 45)
	 }
	 objCanvas.innerHTML="<canvas id='graph' height='278' width='" + intWidth + "'></canvas>";
	//objCanvas.innerHTML="<canvas id='graph' height='278' width='640'></canvas>";
	  fndrawGraph();
}


/* Forward a request to Assigned Task to User
// @ param assignObj "member Name"
// call function fnSendRequest(reqInput)	
*/
function fnAssignTask(assignObj)
{
	strInput = strAssigndTask;
	strMemberName=assignObj;
	assignedMember=document.getElementById("vstatus_" + assignObj).innerHTML;
	reqInput = strInput+"split"+assignObj ;
	if (strInput=="ap")
	{
		heighlitedItem = objSystemDate[intTurnNO-1] ;
	}
	
	fnSendRequest(reqInput);	
	
}





/* Forward a request to  UnAssigned  a Task to User 
// @ param unAssignObj "Player Name"
// call function fnSendRequest(unAssignTaskReq)
// Unassign The task from the player
*/
function fnUnAssign(unAssignObj)
{
	unassignMember=document.getElementById("vstatus_" + unAssignObj).innerHTML;
	unAssignTaskReq = "unAssign"+"split"+unAssignObj;
    unAssignObj = "" ;
    fnSendRequest(unAssignTaskReq);
}




/* forward a request to end the turn 
// @ param endObj
// call function  fnSendRequest(endTaskReq), resetBackground(),	fnresetmemberStatus()
// set responce of the server after endTurn
*/
function fnTurnEnd(endObj)
{
	boolendTurn=true;
	gaintHighlightedItems[gaintHighlightedItems.length] = heighlitedItem;
	if(endObj == "endTurn")
	{
		endTaskReq = endObj+"split" + heighlitedItem;
	}
	else
	endTaskReq = endObj+"split";
//	objMessageContent.innerHTML="";
//	fnSendRequest(endTaskReq);
	resetBackground();
//	fnresetmemberStatus();
	boolTaskStatus=false;
	strAssigndTask="";
	
}



/* Send the Request to Server*/
function fnSendRequest(requestInput)
{
	objAssemFrm = document.getElementById("frmTask");
	objAssemFrm.reset();
	inputData = requestInput ;
	url = "/execute" ;
	requestInput = null ;
        // To remove IE bug :
        if (navigator.appName =="Netscape")
	{
		http_request.open("post", url, true);
	}
        else
        {
		http_request.open("post", url, true);
        }
	http_request.onreadystatechange = fnRequestStatusChanged;
	
	http_request.setRequestHeader("Connection", "close");
        http_request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        
	http_request.send("input="+inputData);		
}


/* Create a Http Request Object*/
function fnCreateObject()
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
http_request = fnCreateObject();


/* Forward a request to get Data for Graph
// @ param graphData 
// call function fndrawGraph
*/

function fnGetGraphData(graphData)
{
	arrDataPopulation = new Array() ;
	arrPopulationleFive =new Array();
	arrPopulationlbetFive =new Array();
	arrpopulationlabovefifteen =new Array();
	var splitGraphData = graphData.split("$$");
    var intWidth;
	var version = parseFloat(navigator.appVersion.split("MSIE")[1]);
//	alert(splitGraphData.length);
	totalPopulation="0";
	populationlefive = "0";	
	populationlbetfive = "0";
	populationlabovefifteen = "0";
	arrDataPopulation.push(totalPopulation);
	arrPopulationleFive.push(populationlefive);
	arrPopulationlbetFive.push(populationlbetfive);
	arrpopulationlabovefifteen.push(populationlabovefifteen);
	for (var i=0; i<splitGraphData.length ; i++ )
	{
		var atempData=splitGraphData[i];
		if (atempData!="")
		{
			dataTemp=atempData.split("@@");
			if (dataTemp[0]!="?"){
				totalPopulation = dataTemp[0];
				populationlefive = dataTemp[1];
				populationlbetfive = dataTemp[2];
				populationlabovefifteen = dataTemp[3];
				}
			
		
		arrDataPopulation.push(totalPopulation);
		arrPopulationleFive.push(populationlefive);
		arrPopulationlbetFive.push(populationlbetfive);
		arrpopulationlabovefifteen.push(populationlabovefifteen);
		objCanvas.innerHTML="";
		var objgraphSection=document.getElementById("graphSection");
		if (splitGraphData.length < 11)
		  {
		   intWidth = 650;
		  }
		  else
		  {
		   intWidth = 650 + ((splitGraphData.length - 10) * 45);
		   
		   if (browser=="Microsoft Internet Explorer")
			{
				   if (version>=7)
				   {   
					  objgraphSection.style.height="290px";
					  objgraphSection.style.marginTop="5px"; 
					  objgraphSection.style.overflowX="auto";
  					  objgraphSection.style.overflowY="hidden";
				   }else if(version==6){
					  objgraphSection.style.height="290px";
					  objgraphSection.style.marginTop="10px";
				   }

			}else{
				objgraphSection.style.height="290px";
				objgraphSection.style.marginTop="5px";
			}
		}
		  objCanvas.innerHTML="<canvas id='graph' height='278' width='" + intWidth + "'></canvas>";
		  try
		  {
		  objgraphSection.scrollLeft = intWidth + 100;		  	
		  }
		  catch (e)
		  {
		  }
		//objCanvas.innerHTML="<canvas id='graph' height='278' width='650'></canvas>";
		fndrawGraph();
		}
	}
}