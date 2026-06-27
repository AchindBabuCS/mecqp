const papersearch=document.querySelector("#papersearch");
papersearch.addEventListener("submit", searchValidate);

function searchValidate(event)
{
    var scheme=document.querySelector("#Scheme");
    var branch=document.querySelector("#Branch");
    var semester=document.querySelector("#Semester");
    var exam_type=document.querySelector("#Exam_Type");
    var month=document.querySelector("#Month");
    var year=document.querySelector("#Year");
    var subject_code=document.querySelector("#Subject_Code");
    var subject=document.querySelector("#Subject");
    if(scheme.value=="Select")
    {
        event.preventDefault();
        alert("Scheme cannot be empty");
        return false;
    }
    if(branch.value=="Select")
    {
        event.preventDefault();
        alert("Branch cannot be empty");
        return false;
    }
    if(semester.value=="Select")
    {
        event.preventDefault();
        alert("Semester cannot be empty");
        return false;
    }
    if(exam_type.value=="Select")
    {
        event.preventDefault();
        alert("Exam Type cannot be empty");
        return false;
    }
    if(month.value=="Select")
    {
        event.preventDefault();
        alert("Month cannot be empty");
        return false;
    }
    if(year.value=="Select")
    {
        event.preventDefault();
        alert("Year cannot be empty");
        return false;
    }
    return true;
}