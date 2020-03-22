//USEUNIT ExcelUnits   
//USEUNIT CTplatformLibrary
//USEUNIT GeneralUnits
//USEUNIT GeneralVariables
//USEUNIT Library
//USEUNIT PDUnits
//USEUNIT PrefetchLibrary
//USEUNIT ProcessingLibrary
//USEUNIT State
//USEUNIT PictorialIndexLibrary


//******Auto Refresh*************************************************************


// Toggle from grid veiw to Pictorial index
function PIToggle()
{
    //Click on toggle button
  Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolPanel"]["rightPanel"]["SplitContainer"]["SplitterPanel_1"]["bottomPanel"]["tabControl"]["seriesPage"]["toggleButton"]["Click"]();
  Wait(5);
  var PI=Aliases["PatientDirectory"]["PatientDirectoryForm"]["FindChild"]("ClrClassName","PictorialIndexPanel",100); 
  if(PI["VisibleOnScreen"])
  {
    Log["Checkpoint"]("Series Thumbnail view is displayed on toggling")
    status2=true
  }
  else
  {
   Log["Error"]("Series Thumbnail view is not displayed on toggling")
   status2=false
  }
  return status2;
}

// finding Pictorial index in PD  
function GetPictorialIndex()
{
  var panelMain = Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolPanel"]["rightPanel"]["SplitContainer"]["SplitterPanel_1"]["bottomPanel"];
  var propValues = new Array( "ClrClassName", "Visible" );
  var varValues = Array( "PictorialLayoutControl", true );
  var pictorialLayout = panelMain["FindChild"](propValues, varValues, 30);
  return pictorialLayout;  
}

// Getting series number by passing description in pictorial index mode 
function GetPictorialIndexSeriesNobyDescription(description)
{
   var pictorialLayout = GetPictorialIndex();
   var indexstatus = false;
   var picounts = pictorialLayout["Controls"]["Count"];
     
   for(var i=0; i<picounts;i++)
   {
     if(description == pictorialLayout["Controls"]["Item_2"](i)["Card"]["Tag"]["SERIES_DESCRIPTION"])
     {
      Log["Message"](i)
      indexstatus = true;
      var seriesno = pictorialLayout["Controls"]["Item_2"](i)["Card"]["Tag"]["SERIES_NUMBER"]
      return seriesno;
      break;
     }
  }
  
  if(!indexstatus)
  {
   Log["Checkpoint"]("Series not found");
  }
}

// Selecting series by passing series number in pictorial index mode from pacs node
function SelectPictorialSeriesBySeriesValue(series)
{
  /*User parameters*/
  //index =Enter the index of the required series to be selected
  //series grid
  
  seriesno=series["split"](",");  
  var indexstatus = false; 
  var v = -1; 
  var pictorialLayout = GetPictorialIndex();
  var picounts = pictorialLayout["Controls"]["Count"];
  //unselect all index's
  for(var i=0; i<picounts;i++) 
  {
    pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](false); 
  }
  //select matched value and exit with value of the index
  for(var testj=0;testj<seriesno["length"];testj++)
  {  
    indexstatus = false;
    for(var i=0; i<picounts;i++)
    {
       if(seriesno[testj] == pictorialLayout["Controls"]["Item_2"](i)["Card"]["Tag"]["SERIES_NUMBER"])
       {
        Log["Message"](i)
        indexstatus = true;
        pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](true);
        v = i;
       }
    }
  }
  
  if(!indexstatus)
  {
   Log["Checkpoint"]("Series not found");
  }
  return v;          
}
 
// Selecting series  by passing series number and description in pictorial index mode from local nodes    
function SelectPictorialSeriesByIndexvalue(series,description)
{
  /*User parameters*/
  //index =Enter the index of the required series to be selected
  //series grid
  var indexstatus = false;
//  var description = "19376";
//  var series = "10232";
  
  var pictorialLayout = GetPictorialIndex();
  var picounts = pictorialLayout["Controls"]["Count"];
  //unselect all index's
  for(var i=0; i<picounts;i++) 
  {
    pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](false); 
  }
  //select matched value and exit with value of the index
  for(var i=0; i<picounts;i++)
  {
     if(description == pictorialLayout["Controls"]["Item_2"](i)["Card"]["Tag"]["SERIES_DESCRIPTION"])
     {
      Log["Message"](i)
      indexstatus = true;
      pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](true);
      return i;
      break;
     }
  }
  
  if(!indexstatus)
  {
   Log["Checkpoint"]("Series not found");
  }          
}   

//*********************************************************************************************************************

function PIContextMenuCopyTo(folderType,folderName)
{
  /*User parameters*/ 
    //folderType=Enter either Local or Remote
    //folderName=Enter the name of the folder to copy
  
  var panelMain = Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolPanel"]["rightPanel"]["SplitContainer"]["SplitterPanel_1"]["bottomPanel"];
  var propValues = new Array( "ClrClassName", "Visible" );
  var varValues = Array( "PictorialLayoutControl", true );
  var pictorialLayout = panelMain["FindChild"](propValues, varValues, 30);
  
    pictorialLayout["ClickR"](50,50);
    ContextMenu("Copy To") 
    var copyDialogBox=Aliases["PatientDirectory"]["CopyToDialog"];
    if(copyDialogBox["resetButton"]["Enabled"])
    {
      copyDialogBox["resetButton"]["ClickButton"]();
    }
    if(copyDialogBox["Exists"])
    {
       if(VarToStr(folderType)=="Local")
       {
         var folderCount=copyDialogBox["Matrices"]["Item"](0)["Buttons"]["Count"];
         var matrix=copyDialogBox["Matrices"]["Item"](0);
         var prop=new Array("WndCaption","Visible");
         var val=new Array("Local Devices",true);
         var location=copyDialogBox["FindChild"](prop,val,100);
       }
       else if(VarToStr(folderType)=="Remote")
       {
         folderCount=copyDialogBox["Matrices"]["Item"](1)["Buttons"]["Count"];
         var matrix=copyDialogBox["Matrices"]["Item"](1);
         var prop=new Array("WndCaption","Visible");
         var val=new Array("Remote Devices",true);
         var location=copyDialogBox["FindChild"](prop,val,100);
       }
         var copied=false;
         for(var i=0; i<folderCount;i++)
         {
            var folder=VarToStr(matrix["Buttons"]["Item"](i)["Text"]["OleValue"]);   
            if(folder==folderName)
            {
               copied=true;
               var X=matrix["Buttons"]["Item"](i)["location_2"]["X"];
               var Y=matrix["Buttons"]["Item"](i)["location_2"]["Y"];
               Wait(1);
               location["Click"](X+10,Y+10);
               Wait(2);
               copyDialogBox["okButton"]["Click"]();
               break;
            }
         }
          if(!copied)
          {
              Aliases["PatientDirectory"]["CopyToDialog"]["cancelButton"]["Click"]();
              Wait(1);
              Log["Error"]("Required folder not found"+folderName);
          }
    }
    else
    {
      Log["Error"]("copyDialogbox doesnot exist");
    }
    Wait(2);
}
//********* Select series

function SeriesSelect(index)
{
  var properties;
  var values;
  
  properties = new Array("Name","Visible");
  values = new Array("[\"WinFormsObject\"](\"tabControl\"))","True");
  
  var SeriesTab = Sys["Process"]("PatientDirectory")["WinFormsObject"]("PatientDirectoryForm")["WinFormsObject"]("mainContainerPanel")["WinFormsObject"]("rightPanel")["WinFormsObject"]("SplitContainer", "", 1)["WinFormsObject"]("SplitterPanel", "", 2)["FindChild"](properties, values, 100);
  
  for(var i=0; i < SeriesTab["TabCount"];i++)
  { 
    if(i==1)
    continue;
    
    delay(1000);
    SeriesTab["ClickTab"](SeriesTab["wTabCaption"](i));    
    Log["Message"]("Select tab is"+SeriesTab["SelectedIndex"]+ " "+SeriesTab["CanFocus"]);
    
    if(i ==  index)
    break;
  }
}

//************************************************************** 

function ChangePatientDetails(fName,lName,DefaultDevice)
{
    //WorklistLibrary["ContextMenu"]("Change Patient Details");
    var CPD=Aliases["PatientDirectory"]["CPD"]
    CPD["WaitProperty"]("Exists", true, 30000);
    //Click on confirmation msg
    Aliases["PatientDirectory"]["PmsMessageBox"]["OK"]["Click"]();
    Wait(1);
    if(fName!="")
    {
        CPD["firstName"]["SetText"](fName)  
    }
    if(lName!="")
    {
       CPD["lastName"]["SetText"](lName)  
    }
    Sys["Process"]("PatientDirectory")["WinFormsObject"]("CreateNewStudyForm")["WinFormsObject"]("raisedPanel")["WinFormsObject"]("chooseDevicesButton")["ClickButton"]()
    
    Choosefolder("Local",DefaultDevice)
    //Click on save
    CPD["save"]["ClickButton"]();
    Wait(1);
    Sys["Process"]("PatientDirectory")["WinFormsObject"]("PmsMessageBox")["WinFormsObject"]("Yes")["Click"]();    
    ProgressBar();  
} 
//**************************************************************

function DeidentifyPatientDetails(lName,DefaultDevice)
{    
  var dpd = Sys["Process"]("PatientDirectory")["WinFormsObject"]("AnonymiseForm");
  dpd["WaitProperty"]("Exists", true, 30000);
  Sys["Process"]("PatientDirectory")["WinFormsObject"]("PmsMessageBox")["WinFormsObject"]("OK")["ClickButton"]();
  //Sys["Process"]("PatientDirectory")["WinFormsObject"]("AnonymiseForm")["WinFormsObject"]("raisedPanel")
  var arrys = new Array("ClrClassName","Name", "Visible");
  var values = new Array("PmsToolPanel","[\"WinFormsObject\"](\"raisedPanel\")",true ); 
  var panel = dpd["FindChild"](arrys,values,100)["WinFormsObject"]("patientDetailsPanel");
   
  if(lName!="" )
  {
    panel["WinFormsObject"]("lastNameTextBox")["SetText"](lName)
  } 
  Sys["Process"]("PatientDirectory")["WinFormsObject"]("AnonymiseForm")["WinFormsObject"]("raisedPanel")["WinFormsObject"]("chooseDevicesButton")["ClickButton"]()
   
  Choosefolder("Local",DefaultDevice)
  //Click on save
  dpd["WinFormsObject"]("saveButton")["ClickButton"](); 
  Sys["Process"]("PatientDirectory")["WinFormsObject"]("PmsMessageBox")["WinFormsObject"]("Yes")["Click"](); 
  ProgressBar();     
} 

//**************************************************************
 
function Choosefolder(folderType,folderName)
{ 
  /*User parameters*/
  //folderType=Enter either Local or Remote
  //folderName=Enter the name of the folder to copy
  //Copy dialog box
  Wait(2);
  var copyDialogBox=Aliases["PatientDirectory"]["CopyToDialog"];
  if(copyDialogBox["resetButton"]["Enabled"])
  {
    copyDialogBox["resetButton"]["ClickButton"]();
  }
  if(copyDialogBox["Exists"])
  {
    if(VarToStr(folderType)=="Local")
    {
      var folderCount=copyDialogBox["Matrices"]["Item"](0)["Buttons"]["Count"];
      var matrix=copyDialogBox["Matrices"]["Item"](0);
      var prop=new Array("WndCaption","Visible");
      var val=new Array("Local Devices",true);
      var location=copyDialogBox["FindChild"](prop,val,100);
    }
    else if(VarToStr(folderType)=="Remote")
    {
      folderCount=copyDialogBox["Matrices"]["Item"](1)["Buttons"]["Count"];
      var matrix=copyDialogBox["Matrices"]["Item"](1);
      var prop=new Array("WndCaption","Visible");
      var val=new Array("Remote Devices",true);
      var location=copyDialogBox["FindChild"](prop,val,100);
    }
    var copied=false;
    for(var i=0;i<folderCount;i++)
    {
      var folder=VarToStr(matrix["Buttons"]["Item"](i)["Text"]["OleValue"]);   
      if(folder==folderName)
      {
        if(matrix["Buttons"]["Item"](i)["Enabled"])
        {
         copied=true;
         var X=matrix["Buttons"]["Item"](i)["location_2"]["X"];
         var Y=matrix["Buttons"]["Item"](i)["location_2"]["Y"];
         Wait(1);
         location["Click"](X+10,Y+10);
         Wait(2);
         copyDialogBox["okButton"]["Click"]();
         break;
        }
        else
        {     
          Log["Error"]("Folder "+folderName+" is not enabled ");
          AddCheckpointResultToReport(false,"","Folder "+folderName+" is not enabled ");  
          break;
        }
      }
    }
    if(!copied)
    {
      Aliases["PatientDirectory"]["CopyToDialog"]["cancelButton"]["Click"]();
      Wait(1);
      AddCheckpointResultToReport(false,"","Required folder not found"+folderName); 
      Log["Error"]("Required folder not found"+folderName);
    }
  }
  else
  {
    Log["Error"]("copyDialogbox doesnot exist");
    AddCheckpointResultToReport(false,"","copyDialogbox doesnot exist"); 
    return false;
  }
  Wait(2);
  return copied;
}

//******************************************************************************

function ProgressBar()
{ 
  var pdProc = Sys["Process"]("PatientDirectory") 
  var prop = new Array( "ClrClassName","Visible" );
  var Val = new Array("PmsProgressBar",true ); 
  var progressBar= pdProc["FindChild"](prop,Val, 100);
  if(progressBar["Exists"])
  {
    var citimeOut = 0;
    while(progressBar["Exists"])
    {
     //waiting for prgores bar to complete
     Delay(1000, "waiting for progess bar to complete")
    	citimeOut++;
    	if(citimeOut > 300)
    		break; 
    }
  Log["Message"]("Change Patient Details successful");
  return true;  
  }
  else
  {
    properties = new Array( "ClrClassName", "Visible" );
    values = new Array("PmsStatusInformationCombo",true ); 
    var messageForm= pdProc["FindChild"](properties, values, 100);
    var messageCount=messageForm["Items"]["Count"]-1;
    var message=messageForm["Items"]["Item"](messageCount)["Message"]["OleValue"];
    if(message=="Change Patient Details successfully completed.  1 entries were saved. Some instances were ignored.  " ||    
    message=="Change Patient Details operation started")
    {
      Log["Message"]("Change Patient Details successful");
      return true
    }
    else
    {
      Log["Error"]("Progress bar not found"); 
      return false;
    }
  } 
}

//******************************************************
function VerifyCSROIApplication()
{
  var calciumScoring;
  var CSMainScene;
  var pmsToolPanel;
  var tableLayoutPanel;
  var pmsComboBox;
  var fieldname = new Array(); 
  var fieldvalue = new Array();
  var afterfieldname = new Array(); 
  var afterfieldvalue = new Array();
  var check =  true;
  var ispib = aqConvert["VarToBool"](ReadLoginSheet("pibMachine"));    
  var process = "PortalAppletHost";
  if(ispib)
  process = "PortalAppletHost64";
  
  calciumScoring = Sys["Process"](process);         
  Wait(3)
        
  properties = new Array("ClrClassName","Name", "Visible");        
  values = new Array("GridControl","[\"WinFormsObject\"](\"gridControl1\")", true);
  imagegrid  = calciumScoring["FindChild"](properties, values, 100);
  gridcolcount = imagegrid["DataSource"]["Columns"]["Count"];        
  for(var i = 0;i<gridcolcount;i++)
  {
    if(imagegrid["DataSource"]["Columns"]["Item"](i)["Caption"]=="Total Coronaries")
    {
      temp = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Count"];
      for(var j = 0;j<temp;j++) 
      {
        //Log["Message"](j+" value"+imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"] )
        fieldvalue[j] = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"]             
      } 
    }
    
    if(imagegrid["DataSource"]["Columns"]["Item"](i)["Caption"]=="RowName")
    {
      temp = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Count"];
      for(var j = 0;j<temp;j++) 
      {
        //Log["Message"](j+" value"+imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"] ) 
        fieldname[j] = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"]              
      }     
    }
  } 
  Wait(3)
  
  properties = new Array("Name", "Visible");        
  values = new Array("[\"WinFormsObject\"](\"manualSeed\")", true);
        
  manualseed = calciumScoring["FindChild"](properties,values, 100)["WinFormsObject"]("comboButton");
  manualseed["Click"]() 
           
  properties = new Array("ClrClassName", "Visible");
  values = new Array("ImageViewer", "True");
  
  imageViewer = calciumScoring["FindChild"](properties, values, 100)
  imageViewer["Click"](575, 216);
  imageViewer["Click"](600, 216);
  Wait(3)
  
  for(var i = 0;i<gridcolcount;i++)
  {
    if(imagegrid["DataSource"]["Columns"]["Item"](i)["Caption"]=="Total Coronaries")
    {
      temp = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Count"];
      for(var j = 0;j<temp;j++) 
      {
        //Log["Message"](j+" value"+imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"] )
        afterfieldvalue[j] = imagegrid["DataSource"]["Columns"]["Item"](i)["Table"]["Rows"]["Item"](j)["Item"](i)["OleValue"]                
      } 
    }
  }
     
  for(var i=0;i<fieldvalue["length"];i++)
  {
    if(fieldvalue[i]!=afterfieldvalue[i])
    {
      Log["Checkpoint"](fieldname[i]+ " Before ROI value is "+fieldvalue[i]+" After ROI value is "+afterfieldvalue[i]);
      check =  true;
    }
    else
    {
      Log["Error"](fieldname[i]+ " Before ROI value is "+fieldvalue[i]+" After ROI value is "+afterfieldvalue[i]);
      check =  false;
      break;
    }
  }
  
  for (var i = 0; i <imageViewer["ImagePresentationState"]["ImageRelativeAnnotators"]["Count"] ; i++)
  {
  roi = imageViewer["ImagePresentationState"]["ImageRelativeAnnotators"]["Item"](i)["ClrClassName"] 
  if (roi == "CsMFHCAnnotator")
  {
    Log["Checkpoint"]("ROI is available on ImageViewer")
    check =  true;
    break;      
  }
}
 return check; 
}

//************************
function SelectPISeriesByMouseHover(series)
{ 
    var pictorialLayout = GetPictorialIndex();
    var seriesbefore =  pictorialLayout["Controls"]["Count"]
    SelectPictorialSeriesBySeriesValue(series)
    var x;
    var y;
    var width;
    var height;
    pictorialLayout["VerticalScroll"]["EnableScroll"](true)
    for(var i=0;i<seriesbefore;i++)
    {
     if(series == pictorialLayout["Controls"]["Item_2"](i)["Card"]["Tag"]["SERIES_NUMBER"])
     {
      indexstatus = true;
      pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](true);
      x =pictorialLayout["Controls"]["Item_2"](i)["Location"]["X"];
      y = pictorialLayout["Controls"]["Item_2"](i)["Location"]["Y"];
      width = pictorialLayout["Controls"]["Item_2"](i)["Width"] 
      height =  pictorialLayout["Controls"]["Item_2"](i)["Height"]  

      pictorialLayout["HoverMouse"](x + (width/2) , y + (height/2))
      pictorialLayout["ClickR"](x + (width/2) , y + (height/2))
      Delay(5000)
      break;
     }
    }           
}

function RightClickPISelectedSeries()
{
  var pictorialLayout = GetPictorialIndex();
  var seriesbefore =  pictorialLayout["Controls"]["Count"]
  for(var i=0;i<seriesbefore;i++)
  {
    if(pictorialLayout["Controls"]["Item"](i)["Card"]["Selected"])
     {
      indexstatus = true;
      pictorialLayout["Controls"]["Item"](i)["Card"]["set_Selected"](true);
      x =pictorialLayout["Controls"]["Item_2"](i)["Location"]["X"];
      y = pictorialLayout["Controls"]["Item_2"](i)["Location"]["Y"];
      width = pictorialLayout["Controls"]["Item_2"](i)["Width"] 
      height =  pictorialLayout["Controls"]["Item_2"](i)["Height"]  

      pictorialLayout["HoverMouse"](x + (width/2) , y + (height/2))
      pictorialLayout["ClickR"](x + (width/2) , y + (height/2))
      pictorialLayout["Keys"]("[Esc]");
     }
  }
}

//***********************************************

function PIContextMenuCopyToRighClick(folderType,folderName)
{
  /*User parameters*/ 
    //folderType=Enter either Local or Remote
    //folderName=Enter the name of the folder to copy
  
  var panelMain = Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolPanel"]["rightPanel"]["SplitContainer"]["SplitterPanel_1"]["bottomPanel"];
  var propValues = new Array( "ClrClassName", "Visible" );
  var varValues = Array( "PictorialLayoutControl", true );
  var pictorialLayout = panelMain["FindChild"](propValues, varValues, 30);
  
    //pictorialLayout["ClickR"](50,50);
    ContextMenu("Copy To") 
    var copyDialogBox=Aliases["PatientDirectory"]["CopyToDialog"];
    if(copyDialogBox["resetButton"]["Enabled"])
    {
      copyDialogBox["resetButton"]["ClickButton"]();
    }
    if(copyDialogBox["Exists"])
    {
       if(VarToStr(folderType)=="Local")
       {
         var folderCount=copyDialogBox["Matrices"]["Item"](0)["Buttons"]["Count"];
         var matrix=copyDialogBox["Matrices"]["Item"](0);
         var prop=new Array("WndCaption","Visible");
         var val=new Array("Local Devices",true);
         var location=copyDialogBox["FindChild"](prop,val,100);
       }
       else if(VarToStr(folderType)=="Remote")
       {
         folderCount=copyDialogBox["Matrices"]["Item"](1)["Buttons"]["Count"];
         var matrix=copyDialogBox["Matrices"]["Item"](1);
         var prop=new Array("WndCaption","Visible");
         var val=new Array("Remote Devices",true);
         var location=copyDialogBox["FindChild"](prop,val,100);
       }
         var copied=false;
         for(var i=0;i<folderCount;i++)
         {
            var folder=VarToStr(matrix["Buttons"]["Item"](i)["Text"]["OleValue"]);   
            if(folder==folderName)
            {
               copied=true;
               var X=matrix["Buttons"]["Item"](i)["location_2"]["X"];
               var Y=matrix["Buttons"]["Item"](i)["location_2"]["Y"];
               Wait(1);
               location["Click"](X+10,Y+10);
               Wait(2);
               copyDialogBox["okButton"]["Click"]();
               break;
            }
         }
          if(!copied)
          {
              Aliases["PatientDirectory"]["CopyToDialog"]["cancelButton"]["Click"]();
              Wait(1);
              Log["Error"]("Required folder not found"+folderName);
          }
    }
    else
    {
      Log["Error"]("copyDialogbox doesnot exist");
    }
    Wait(2);
}

//*********************
function runNetworkLogin()
{
    var Tasks, Task;
    // Run Login in CLient B
    Tasks = NetworkSuite["Jobs"]["ItemByName"]("Login")["Tasks"];
    Task = Tasks["Items"](0);
    Task["Run"](true);
}

function runNetworkLogout()
{
      var Tasks, Task;
    // Run Login in CLient B
    Tasks = NetworkSuite["Jobs"]["ItemByName"]("Login")["Tasks"];   
    Task = Tasks["Items"](2);
    Task["Run"](true);
}

//*****************************
function SeriesReportCount()
{
  var seriesPanel=Sys["Process"]("PatientDirectory")["FindChild"]("ClrClassName","ReportPanel",100);
  var grid=seriesPanel["FindChild"]("ClrClassName","BoundColumnSelectedGrid",100);
  var seriesCount=grid["Views"]["Item"](0)["DataRowCount"];
  return seriesCount;
}

//****************************
function SeriesFilesCount()
{
  var seriesPanel=Sys["Process"]("PatientDirectory")["FindChild"]("ClrClassName","filePanel",100);
  var grid=seriesPanel["FindChild"]("ClrClassName","BoundColumnSelectedGrid",100);
  var seriesCount=grid["Views"]["Item"](0)["DataRowCount"];
  return seriesCount;
}

//**************
function AutoRefreshImport(path,folderName,MRstudy_vendor)
{
  /*User parameteers*/
  //path=Enter the path of the source folder
  //folderName=Enter the name of the folder to be imported.

   //Folder button
  var gridcount ;
  var pdcount ;
  var flag =0;
  var status1 = false;
  var status2 = false;

  var pdProc = Sys["Process"]("PatientDirectory")
  properties = new Array( "ClrClassName","Name", "Visible" );
  values = new Array("PmsButtonMatrixCombo","[\"WinFormsObject\"](\"matrixCombo\")",true ); 
  var folderSpace= pdProc["FindChild"](properties, values, 100);
  if(folderSpace["Exists"])
  {
    folderSpace["ClickR"]();
    //calling context menu
    ContextMenu("Import Data");
    //Import dialog box
    var importDialog= pdProc["WinFormsObject"]("PmsImportDialog");
    if(importDialog["Exists"])
    {
      //Source path edit box
      var sourcePath=importDialog["WinFormsObject"]("panel2")["WinFormsObject"]("pathHistoryCombo");
      sourcePath["SetText"](path);
      sourcePath["Keys"]("[Enter]");
           
      //Selecting required source folder
      var propVal = new Array( "ClrClassName","Visible" );
      var varVal = new Array("FileSystemListView",true ); 
      var sourceFolder= pdProc["FindChild"](propVal, varVal, 100);
      sourceFolder["ClickItem"](folderName);
      var okButton= importDialog["WinFormsObject"]("panel3")["WinFormsObject"]("panel1")["WinFormsObject"]("btnOK")
      okButton["Click"]();
      Log["Message"]("Clicking on ok button");
      Wait(1);
           
      //Progress bar
      var prop = new Array( "ClrClassName","Visible" );
      var Val = new Array("PmsProgressBar",true ); 
      var progressBar= pdProc["FindChild"](prop,Val, 100);
      if(progressBar["Exists"])
      {
        while(progressBar["Exists"])
        {        
          if(progressBar["Value"] > 25 && progressBar["Value"] < 30 && flag == 0)
          {
            gridcount = StudyCount();
            pdcount = CopyDeleteLibrary["GetStudyCounts"]("Display");
          
            if(gridcount == pdcount)
            {
              Log["Message"](" Study counts are equal");
              status1 = true;
            }
            else
            Log["Warning"]("Study counts are not equal")
          
            flag = 1;
          }
        
          if(progressBar["Value"] > 50 && progressBar["Value"] < 55 && flag == 1)
          {         
            SelectPatient(MRstudy_vendor);
            if(flag == 1)
            {
              status2 = VerifyisPatientSelected(MRstudy_vendor);
              if(status2)
              {
                Log["Message"](MRstudy_vendor+" study is marked with blue background");
              }
              else
              {
                Log["Warning"](MRstudy_vendor+"study is not marked with blue background");
                status1 = false;  
              }
              flag = 2;
             } 
          }
        
          if(progressBar["Value"] > 70 && progressBar["Value"] < 75 && flag == 2)
          {
            ARSorting("Patient Name","Ascending",true);
            SelectPatient(MRstudy_vendor);
            status2 = VerifyisPatientSelected(MRstudy_vendor);
            if(status2)
            {
              Log["Message"](MRstudy_vendor+" study is marked with blue background after sorting in ascending order");
            }
            else
            {
              Log["Warning"](MRstudy_vendor+"study is not marked with blue background after sorting in ascending order");
              status1 = false;  
            }
            flag = 3;
          }
      
          if(progressBar["Value"] > 90 && progressBar["Value"] < 95 && flag == 3)
          {
            ARSorting("Patient Name","Descending",true);
            SelectPatient(MRstudy_vendor);
            status2 = VerifyisPatientSelected(MRstudy_vendor);
            if(status2)
            {
              Log["Message"](MRstudy_vendor+" study is marked with blue background after sorting in descending order");
            }
            else
            {
              Log["Warning"](MRstudy_vendor+"study is not marked with blue background after sorting in descending order");
              status1 = false;  
            }
            flag = 4;
          }
          Wait(1);
        }
        return status1;
      }
      else
      {
       properties = new Array( "ClrClassName", "Visible" );
       values = new Array("PmsStatusInformationCombo",true ); 
       var messageForm= pdProc["FindChild"](properties, values, 100);
       var messageCount=messageForm["Items"]["Count"]-1;
       var message=messageForm["Items"]["Item"](messageCount)["Message"]["OleValue"];
       if(message=="Import Ended")
       {
         Log["Message"]("Import successful");
         return true
       }
       else
       {
         Log["Error"]("Progress bar not found"); 
         return false;
       }
      }  
    }
    else
    {
       Log["Error"]("ImportDialog doesn't exist");
       return false;
    }
  }
  else
  {
   Log["Error"]("Folder space doesn't exists");
   return false;
  } 
}

function VerifyisPatientSelected(pname)
{

  var studyGrid = StudyGrid();
  
  var rowCount= studyGrid["DataSource"]["Table"]["Rows"]["Count"];
  for(var j=0;j<rowCount;j++)
  {
    Wait(1);
    if(studyGrid["FocusedView"]["GetDataRow"](j)["PATIENTS_NAME"] ==pname)
    { 
      Wait(2);
      Log["Message"](studyGrid["FocusedView"]["GetDataRow"](j)["IsBlueSelected"])
      if(studyGrid["FocusedView"]["GetDataRow"](j)["IsBlueSelected"]==true)
       { 
        status=true
        Log["Message"]("Selected study is marked with blue background");
       }
      else
      {
        status=false
        Log["Error"]("Selected study is not marked with blue background");
      }
    }
  }
  return status;
}

function ARSorting(columnName,sortingOrder,study)
{
  /*User parameters*/
  //columnName=Enter the field name to be sorted
  //sortingOrder=Enter Ascending or Descending
  //bool Study=Enter true for sorting study grid ,false for series grid.
  var commonGrid= Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolPanel"]["rightPanel"]["SplitContainer"];
  var prop = new Array( "ClrClassName","Name","Visible" );
  var Val = new Array("BoundColumnSelectedGrid","[\"WinFormsObject\"](\"grid\")",true ); 
       
  //Study grid      
  if(study)
  {
    var grid=commonGrid["SplitterPanel"]["FindChild"](prop,Val, 100);
  }
  else
  { 
    var grid=commonGrid["SplitterPanel_1"]["FindChild"](prop,Val, 100);
  } 
  if(grid["Exists"])
  {
   var columnCount=grid["DefaultView"]["Columns"]["Count"]; 
   for(var i=0;i<columnCount;i++)
   {
     var colName=grid["DefaultView"]["Columns"]["Item_2"](i)["Caption"]["OleValue"];
     if(VarToStr(colName)==VarToStr(columnName))
     {
        // Sorting
        grid["DefaultView"]["Columns"]["Item_2"](i)["set_SortOrder"](sortingOrder);
        break;
     }
   }
  }
  else
  {
    Log["Error"]("grid does not exists");
  }
  Wait(2);
} 

function DeleteAllStudies()
{
  var studygrid = StudyGrid();

  studygrid["Views"]["Item"](0)["SelectAll"]();
  SyncWithStopButton() 
  //Click delete button
  Aliases["PatientDirectory"]["PatientDirectoryForm"]["PmsToolsPanel"]["leftPanel"]["toolbox"]["panel"]["deleteButton"]["Click"]();
  Wait(1);
  //Click yes on confirmation msg
  Aliases["PatientDirectory"]["PmsMessageBox"]["Yes"]["Click"]();
  SyncWithStopButton();
  Wait(5);
}

function RunScriptsinRemoteSystem(RemoteIP,AdminUsername,AdminPassword,BasePath,ProjectSuitePath,HostName)
{        
    // run sanity test cases adding hosts
    var Host = NetworkSuite["Hosts"]["ItemByName"](HostName);
    // Specifies the host's parameters
    Host["Address"] = RemoteIP;
    Host["BasePath"] = BasePath;
    Host["ProjectSourcePath"] = ProjectSuitePath;
    Host["UserName"] = AdminUsername
    Host["Password"] = AdminPassword
    Host["CopyProjectToSlave"]();
  
    // Verifies whether the created host can be used by a network suite
    if (Host["Verify"]() == false) 
    {
    i = MessageDlg(Host["Address"] + " machine not able to find in the network, Execution terminated", mtError, i, 0);  
    return;  
    }
    else
    {
     return true;
    }     
}

