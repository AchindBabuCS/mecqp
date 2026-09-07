const newpaper=document.createElement("div");
const modifypaperform=document.createElement("div");
const newbutton=document.querySelector("#New");
const modifybutton=document.querySelector("#Modify");
const updatebutton=document.querySelectorAll(".Update");
const postformopen=document.querySelector("#postformopen");
const csrfToken=document.querySelector('meta[name="csrf-token"]').getAttribute("content");
for (let i=0; i<updatebutton.length; i++){
    updatebutton[i].addEventListener("click", updatesubmissionform);
}
let formopen=false;
newbutton.addEventListener("click", newsubmission);
modifybutton.addEventListener("click", modifysearchformcheck);
if(postformopen?.value=="true"){
    formopen=true;
}
function newsubmission(event)
{
    if(formopen){
        event.preventDefault();
    }else{
        newpaper.innerHTML=`
        <form method="POST" id="newsubmit" name="newsubmit" enctype="multipart/form-data" onsubmit="return newValidate()">
            <input type="hidden" name="csrf_token" value="${csrfToken}">
            <table id="newinputbox">
                <tr>
                    <th>
                        Scheme
                    </th>
                    <th>
                        Branch
                    </th>
                    <th>
                        Semester
                    </th>
                    <th>
                        Exam Type
                    </th>
                    <th>
                        Month
                    </th>
                    <th>
                        Year
                    </th>
                    <th>
                        Subject Code
                    </th>
                    <th>
                        Subject
                    </th>
                    <th>
                        File
                    </th>
                </tr>
                <tr>
                    <td>
                        <select id="newscheme" name="newscheme">
                            <option>
                                Select
                            </option>
                            <option>
                                2019
                            </option>
                            <option>
                                2024
                            </option>
                        </select>
                    </td>
                    <td>
                        <select id="newbranch" name="newbranch">
                            <option>
                                Select
                            </option>
                            <option>
                                CSE
                            </option>
                            <option>
                                CSBS
                            </option>
                            <option>
                                EC
                            </option>
                            <option>
                                EB
                            </option>
                            <option>
                                EV
                            </option>
                            <option>
                                EEE
                            </option>
                            <option>
                                ME
                            </option>
                        </select>
                    </td>
                    <td>
                        <select id="newsemester" name="newsemester">
                            <option>
                                Select
                            </option>
                            <option>                    
                                1
                            </option>
                            <option>
                                2
                            </option>
                            <option>
                                3
                            </option>
                            <option>
                                4
                            </option>
                            <option>
                                5
                            </option>
                            <option>
                                6
                            </option>
                            <option>
                                7
                            </option>
                            <option>
                                8
                            </option>
                        </select>
                    </td>
                    <td>
                        <select id="newexam_type" name="newexam_type">
                            <option>
                                Select
                            </option>
                            <option>
                                Internal-1
                            </option>
                            <option>
                                Internal-2
                            </option>
                            <option>
                                Semester-R
                            </option>
                            <option>
                                Semester-S
                            </option>
                        </select>
                    </td>
                    <td>
                        <select id="newmonth" name="newmonth">
                            <option>
                                Select
                            </option>
                            <option>
                                January
                            </option>
                            <option>
                                February
                            </option>
                            <option>
                                March
                            </option>
                            <option>
                                April
                            </option>
                            <option>
                                May
                            </option>
                            <option>
                                June
                            </option>
                            <option>
                                July
                            </option>
                            <option>
                                August
                            </option>
                            <option>
                                September
                            </option>
                            <option>
                                October
                            </option>
                            <option>
                                November
                            </option>
                            <option>
                                December
                            </option>
                        </select>
                    </td>
                    <td>
                        <select id="newyear" name="newyear">
                            <option>
                                Select
                            </option>
                            <option>
                                2026
                            </option>
                            <option>
                                2025
                            </option>
                            <option>
                                2024
                            </option>
                            <option>
                                2023
                            </option>
                            <option>
                                2022
                            </option>
                            <option>
                                2021
                            </option>
                            <option>
                                2020
                            </option>
                            <option>
                                2019
                            </option>
                        </select>
                    </td>
                    <td>
                        <input type="text" id="newsubject_code" name="newsubject_code">
                    </td>
                    <td>
                        <input type="text" id="newsubject" name="newsubject">
                    </td>
                    <td>
                        <input type="file" id="newfile" name="newfile">
                    </td>
                    <td>
                        <button type="submit" name="upload" id="newsubmitbutton">
                            Submit
                        </button>
                    </td>
                </tr>
            </table>
        </form>`;
        document.body.appendChild(newpaper);
        formopen=true;
    }
}
function newValidate(){
    var newscheme=document.querySelector("#newscheme");
    var newbranch=document.querySelector("#newbranch");
    var newsemester=document.querySelector("#newsemester");
    var newexam_type=document.querySelector("#newexam_type");
    var newmonth=document.querySelector("#newmonth")
    var newyear=document.querySelector("#newyear");
    var newsubject_code=document.querySelector("#newsubject_code");
    var newsubject=document.querySelector("#newsubject");
    var newfile=document.querySelector("#newfile");
    if(newscheme.value=="Select"){
        alert("Scheme cannot be blank");
        return false;
    }
    if(newbranch.value=="Select"){
        alert("Branch cannot be blank");
        return false;
    }
    if(newsemester.value=="Select"){
        alert("Semester cannot be blank");
        return false;
    }
    if(newexam_type.value=="Select"){
        alert("Exam Type cannot be blank");
        return false;
    }
    if(newmonth.value=="Select"){
        alert("Month cannot be blank");
        return false;
    }
    if(newyear.value=="Select"){
        alert("Year cannot be blank");
        return false;
    }
    if(newsubject_code.value==""){
        alert("Subject Code cannot be blank");
        return false;
    }
    if(newsubject.value==""){
        alert("Subject cannot be blank");
        return false;
    }
    if(newfile.files.length===0){
        alert("File must be uploaded");
        return false;
    }
    return true;
}
function modifysearchformcheck(event)
{
    if(formopen){
        event.preventDefault();
    }else{
        formopen=true;        
    }
}
function modifyValidate()
{
    var modifysearchscheme=document.querySelector("#modifysearchscheme");
    var modifysearchbranch=document.querySelector("#modifysearchbranch");
    var modifysearchsemester=document.querySelector("#modifysearchsemester");
    var modifysearchexam_type=document.querySelector("#modifysearchexam_type");
    var modifysearchmonth=document.querySelector("#modifysearchmonth")
    var modifysearchyear=document.querySelector("#modifysearchyear");
    if(modifysearchscheme.value=="Select"){
        alert("Scheme cannot be empty");
        return false;
    }
    if(modifysearchbranch.value=="Select"){
        alert("Branch cannot be empty");
        return false;
    }
    if(modifysearchsemester.value=="Select"){
        alert("Semester cannot be empty");
        return false;
    }
    if(modifysearchexam_type.value=="Select"){
        alert("Exam Type cannot be empty");
        return false;
    }
    if(modifysearchmonth.value=="Select"){
        alert("Month cannot be empty");
        return false;
    }
    if(modifysearchyear.value=="Select"){
        alert("Year cannot be empty");
        return false;
    }
    return true;
}
function updatesubmissionform(event)
{
    const updatepaperid=event.target.dataset.updatepaperid;
    const updatesubject_code=event.target.dataset.updatesubject_code;
    const updatesubject=event.target.dataset.updatesubject;
    modifypaperform.innerHTML=`
    <form method="POST" id="updatesubmit" name="updatesubmit" onsubmit="return updateValidate()">
        <input type="hidden" name="csrf_token" value="${csrfToken}">
        <table id="updateinputbox">
            <tr>
                <th>
                    Paper ID
                </th>
                <th>
                    Scheme
                </th>
                <th>
                    Branch
                </th>
                <th>
                    Semester
                </th>
                <th>
                    Exam Type
                </th>
                <th>
                    Month
                </th>
                <th>
                    Year
                </th>
                <th>
                    Subject Code
                </th>
                <th>
                    Subject
                </th>
            </tr>
            <tr>
                <td>
                    <input type="text" id="updatepaperid" name="updatepaperid" value="${updatepaperid}" readonly>
                </td>
                <td>
                    <select id="updatescheme" name="updatescheme">
                        <option>
                            Select
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            2019
                        </option>
                        <option>
                            2024
                        </option>
                    </select>
                </td>
                <td>
                    <select id="updatebranch" name="updatebranch">
                        <option>
                            Select  
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            CSE
                        </option>
                        <option>
                            CSBS
                        </option>
                        <option>
                            EC
                        </option>
                        <option>
                            EB
                        </option>
                        <option>
                            EV
                        </option>
                        <option>
                            EEE
                        </option>
                        <option>
                            ME
                        </option>
                    </select>
                </td>
                <td>
                    <select id="updatesemester" name="updatesemester">
                        <option>
                            Select
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            1
                        </option>
                        <option>
                            2
                        </option>
                        <option>
                            3
                        </option>
                        <option>
                            4
                        </option>
                        <option>
                            5
                        </option>
                        <option>
                            6
                        </option>
                        <option>
                            7
                        </option>
                        <option>
                            8
                        </option>
                    </select>
                </td>
                <td>
                    <select id="updateexam_type" name="updateexam_type">
                        <option>
                            Select
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            Internal-1
                        </option>
                        <option>
                            Internal-2
                        </option>
                        <option>
                            Semester-R
                        </option>
                        <option>
                            Semester-S
                        </option>
                    </select>
                </td>
                <td>
                    <select id="updatemonth" name="updatemonth">
                        <option>
                            Select
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            January
                        </option>
                        <option>
                            February
                        </option>
                        <option>
                            March
                        </option>
                        <option>
                            April
                        </option>
                        <option>
                            May
                        </option>
                        <option>
                            June
                        </option>
                        <option>
                            July
                        </option>
                        <option>
                            August
                        </option>
                        <option>
                            September
                        </option>
                        <option>
                            October
                        </option>
                        <option>
                            November
                        </option>
                        <option>
                            December
                        </option>
                    </select>
                </td>
                <td>
                    <select id="updateyear" name="updateyear">
                        <option>
                            Select
                        </option>
                        <option>
                            All
                        </option>
                        <option>
                            2026
                        </option>
                        <option>
                            2025
                        </option>
                        <option>
                            2024
                        </option>
                        <option>
                            2023
                        </option>
                        <option>
                            2022
                        </option>
                        <option>
                            2021
                        </option>
                        <option>
                            2020
                        </option>
                        <option>
                            2019
                        </option>
                    </select>
                </td>
                <td>
                    <input type="text" id="updatesubject_code" name="updatesubjectcode" value="${updatesubject_code}" readonly>
                </td>
                <td>
                    <input type="text" id="updatesubject" name="updatesubject" value="${updatesubject}" readonly>
                </td>
                <td>
                    <button type="submit" name="updatesubmit" id="updatesubmitbutton">
                        Submit
                    </button>
                </td>
            </tr>
        </table>
    </form>`;
    document.body.appendChild(modifypaperform);
    formopen=true;
}
function updateValidate()
{
    var updatescheme=document.querySelector("#updatescheme");
    var updatebranch=document.querySelector("#updatebranch");
    var updatesemester=document.querySelector("#updatesemester");
    var updateexam_type=document.querySelector("#updateexam_type");
    var updatemonth=document.querySelector("#updatemonth")
    var updateyear=document.querySelector("#updateyear");
    if(updatescheme.value=="Select"){
        alert("Scheme cannot be empty");
        return false;
    }
    if(updatebranch.value=="Select"){
        alert("Branch cannot be empty");
        return false;
    }
    if(updatesemester.value=="Select"){
        alert("Semester cannot be empty");
        return false;
    }
    if(updateexam_type.value=="Select"){
        alert("Exam Type cannot be empty");
        return false;
    }
    if(updatemonth.value=="Select"){
        alert("Month cannot be empty");
        return false;
    }
    if(updateyear.value=="Select"){
        alert("Year cannot be empty");
        return false;
    }
    return true;
}
function deleteValidate()
{
    var deletesearchscheme=document.querySelector("#deletesearchscheme");
    var deletesearchbranch=document.querySelector("#deletesearchbranch");
    var deletesearchsemester=document.querySelector("#deletesearchsemester");
    var deletesearchexam_type=document.querySelector("#deletesearchexam_type");
    var deletesearchmonth=document.querySelector("#deletesearchmonth")
    var deletesearchyear=document.querySelector("#deletesearchyear");
    if(deletesearchscheme.value=="Select"){
        alert("Scheme cannot be empty");
        return false;
    }
    if(deletesearchbranch.value=="Select"){
        alert("Branch cannot be empty");
        return false;
    }
    if(deletesearchsemester.value=="Select"){
        alert("Semester cannot be empty");
        return false;
    }
    if(deletesearchexam_type.value=="Select"){
        alert("Exam Type cannot be empty");
        return false;
    }
    if(deletesearchmonth.value=="Select"){
        alert("Month cannot be empty");
        return false;
    }
    if(deletesearchyear.value=="Select"){
        alert("Year cannot be empty");
        return false;
    }
    return true;
}
function rejectValidate(event)
{
    var reason=event.currentTarget.querySelector(".Reason");
    if(reason.value==""){
        alert("Reason must not be blank");
        return false;
    }
    return true;
}
function messageValidate()
{
    var message=document.querySelector("#adminmessage");
    if(message.value==""){
        alert("Message must not be blank");
        return false;
    }
    return true;
}