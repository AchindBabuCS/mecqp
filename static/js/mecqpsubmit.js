const submit=document.querySelector("#submit");
submit.addEventListener("submit", submitValidate);
function submitValidate(event)
    {
        var clickwrap=document.querySelector("#clickwrap");
        var uploadfile=document.querySelector("#file");
        var filedescription=document.querySelector("#description");
        if(uploadfile.files.length===0)
        {
            event.preventDefault();
            alert("File must be uploaded");
            return false;
        }
        var extension=uploadfile.files[0].name.split('.').pop().toLowerCase();
        if(uploadfile.files[0].size>=10*1024*1024)
        {
            event.preventDefault();
            alert("File size too large.");
            return false;
        }
        if(extension!="pdf")
        {
            event.preventDefault();
            alert("File is not in PDF format");
            return false;
        }
        if(filedescription.value=="")
        {
            event.preventDefault();
            alert("Descriptiom cannot be blank");
            return false;
        }
        if(!clickwrap.checked)
        {
            event.preventDefault();
            alert("You have not agreed to Rules and Upload Conditions");
            return false;
        }
        return true;
    }