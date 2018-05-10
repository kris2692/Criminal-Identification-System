function validate()
  {
  
     if( document.myForm.name.value == "" )
     {
        alert( "Please provide a valid name!" );
        document.myForm.name.focus() ;
        return false;
     }
     if( document.myForm.location.value == "" )
     {
        alert( "Please provide a location!" );
        document.myForm.location.focus() ;
        return false;
     }
     if( document.myForm.description.value == "" )
     {
        alert( "Please provide a description!" );
        document.myForm.description.focus() ;
        return false;
     }
     if( document.myForm.date.value == "" )
     {
        alert( "Please provide a valid date!" );
        document.myForm.date.focus() ;
        return false;
     }
     if( document.myForm.image.value == "" )
     {
        alert( "Please provide a valid image!" );
        document.myForm.image.focus() ;
        return false;
     }
return(true);
      }