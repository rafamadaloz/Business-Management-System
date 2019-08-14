$.Admin.tour = {
    init: function () {

        $(".ratings-axis-input input").rating();


        //initialize instance
        var enjoyhint_instance = new EnjoyHint({});

//simple config.
//Only one step - highlighting(with description) "New" button
//hide EnjoyHint after a click on the button.
        var enjoyhint_script_steps = [
            {
                'click .btn_cadastro': 'Bem-vindo ao SGEO ERP. Vamos começar fazendo o cadastro da sua empresa, ' +
                    'clique em "Cadastro"'
            },
            {
                'click .btn_cadastro_empresas': 'Agora vá em "Empresas"'
            }
        ];

//set script config
        enjoyhint_instance.set(enjoyhint_script_steps);

//run Enjoyhint script
        enjoyhint_instance.run();

    }
};

$.Admin.tourPaginaCadastroEmpresa = {
   init: function () {

        $(".ratings-axis-input input").rating();

        //initialize instance
        var enjoyhint_instance = new EnjoyHint({});

//simple config.
//Only one step - highlighting(with description) "New" button
//hide EnjoyHint after a click on the button.
        var enjoyhint_script_steps = [
            {
                'click .botao_adicionar': 'Clique em "Adicionar"'
            },
        ];

//set script config
        enjoyhint_instance.set(enjoyhint_script_steps);

//run Enjoyhint script
        enjoyhint_instance.run();

    }
};