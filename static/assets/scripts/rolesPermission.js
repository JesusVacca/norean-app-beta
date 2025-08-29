window.addEventListener('DOMContentLoaded',function (){
    const buttonsPermission = document.querySelectorAll('.btn-permission');
    const modal = document.querySelector('.modal-custom');

    buttonsPermission.forEach(button=>{
        button.addEventListener('click',()=>{
            modal.classList.toggle('open-modal-custom');
            const tbody = modal.querySelector('.table__body');
            const stringPermissionsDB = button.dataset.permissions;
            const stringPermissionsForRole = button.dataset.permissionsRole;
            const permissionsDB = JSON.parse(stringPermissionsDB)
            const permissionsForRole = JSON.parse(stringPermissionsForRole)


        })
    })
})