
class EmissorNotaMyse:

    token = 'token'

    def cadastro_cliente(self, nota_obj):

        body = {}

        if nota_obj.dest_saida.tipo_pessoa == 'PF':
            body['tipo'] = "F (Física)"
            body['razao_social'] = nota_obj.dest_saida.nome_razao_social
            body['nome_fantasia'] = nota_obj.dest_saida.nome_razao_social
            body['cnpj'] = nota_obj.dest_saida.cpf_cnpj_apenas_digitos
            body['inscricao_municipal'] = nota_obj.dest_saida.inscricao_municipal
        elif nota_obj.dest_saida.tipo_pessoa == 'PJ':
            body['tipo'] = "J (Jurídica)"
            body['nome'] = nota_obj.dest_saida.nome_razao_social
            body['cpf'] = nota_obj.dest_saida.cpf_cnpj_apenas_digitos
            body['rg'] = nota_obj.dest_saida.rg

        body['inscricao_estadual'] = nota_obj.dest_saida.inscricao_estadual

        if nota_obj.dest_saida.telefone_padrao:
            body['contato']["telefone"] = nota_obj.dest_saida.telefone_padrao.get_telefone_apenas_digitos(),

        if nota_obj.dest_saida.email_padrao:
            body['contato']['email'] = nota_obj.dest_saida.email_padrao

        if nota_obj.dest_saida.endereco_padrao:
            body['endereco']['cep'] = nota_obj.dest_saida.endereco_padrao.cep
            body['endereco']['rua'] = nota_obj.dest_saida.endereco_padrao.logradouro
            body['endereco']['numero'] = nota_obj.dest_saida.endereco_padrao.numero
            body['endereco']['complemento'] = nota_obj.dest_saida.endereco_padrao.complemento
            body['endereco']['bairro'] = nota_obj.dest_saida.endereco_padrao.bairro
            body['endereco']['cidade'] = nota_obj.dest_saida.endereco_padrao.cidade
            body['endereco']['estado'] = nota_obj.dest_saida.endereco_padrao.uf

        return 1

    def cadastro_produtos(self, nota_obj):

        for index, item in enumerate(nota_obj.venda.itens_venda.all(), 1):
            produto = {}

            produto['referencia'] = item.produto.codigo
            produto['nome'] = item.produto.descricao
            produto['valor'] = item.valor_unit
            produto['medida'] = item.produto.get_sigla_unidade()
            produto['ncm'] = item.produto.ncm
            produto['anp'] = ""
            produto['origem'] = item.produto.origem

            if item.produto.cfop_padrao:
                produto['cfop-preferencial'] = item.produto.cfop_padrao

            produto['configuracoes-fiscais']['cfop'] = item.produto.cfop_padrao

            # Impostos
            if item.produto.grupo_fiscal:

                #IPI
                ipi_obj = item.produto.grupo_fiscal.ipi_padrao.get()
                if ipi_obj.cst:
                    produto['configuracoes-fiscais']['configuracoes']['ipi']['ipi-cst'] = ipi_obj.cst
                    if ipi_obj.tipo_ipi == '1':
                        produto['configuracoes-fiscais']['configuracoes']['ipi']['ipi-aliquota'] = ipi_obj.valor_fixo
                    elif ipi_obj.tipo_ipi == '2':
                        produto['configuracoes-fiscais']['configuracoes']['ipi']['ipi-aliquota'] = ipi_obj.p_ipi
                else:
                    produto['configuracoes-fiscais']['configuracoes']['ipi']['ipi-cst'] = ipi_obj.cst = '99'

                # PIS
                pis_obj = item.produto.grupo_fiscal.pis_padrao.get()
                if pis_obj.cst:
                    produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['pis-cst'] = pis_obj.cst

                    if pis_obj.valiq_pis:
                        produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['pis-aliquota'] = pis_obj.valiq_pis
                    elif pis_obj.p_pis:
                        produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['pis-aliquota'] = pis_obj.p_pis

                else:
                    produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['pis-cst'] = '99'

                # COFINS
                cofins_obj = item.produto.grupo_fiscal.cofins_padrao.get()
                if cofins_obj.cst:
                    produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['cofins-cst'] = cofins_obj.cst

                    if cofins_obj.valiq_cofins:
                        produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['cofins-cst'] = cofins_obj.valiq_cofins
                    elif cofins_obj.p_cofins:
                        produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['cofins-cst'] = cofins_obj.p_cofins
                else:
                    produto['configuracoes-fiscais']['configuracoes']['pis-cofins']['cofins-cst'] = '99'

    def emitir_nfe(self, nota_obj):

        nfe = {}

        nfe['numero'] = nota_obj.n_nf_saida
        nfe['serie'] = nota_obj.serie
        nfe['cfop'] = nota_obj.natop
        nfe['cliente'] = nota_obj.dest_saida.cpf_cnpj_apenas_digitos
        nfe['tipo'] = nota_obj.tpnf
        if nota_obj.tpnf == '0':
            nfe['tipo'] = 'E (entrada)'
        elif nota_obj.tpnf == '1':
            nfe['tipo'] = 'S (saída)'

        if nota_obj.fin_nfe == '1':
            nfe['finalidade'] = 'N'
        elif nota_obj.fin_nfe == '2':
            nfe['finalidade'] = 'C'
        elif nota_obj.fin_nfe == '3':
            nfe['finalidade'] = 'A'
        elif nota_obj.fin_nfe == '4':
            nfe['finalidade'] = 'D'

        nfe['valor_despesas'] = nota_obj.venda.despesas

        nfe['observacao'] = nota_obj.inf_cpl

        nfe['transporte']['modalidade'] = nota_obj.venda.mod_frete

        if nota_obj.venda.transportadora:
            nfe['transporte']['transportadora'] = nota_obj.venda.transportadora.cpf_cnpj_apenas_digitos

        if nota_obj.venda.veiculo:
            nfe['transporte']['placa-veiculo'] = nota_obj.venda.veiculo.placa
        else:
            nfe['transporte']['placa-veiculo'] = 'AAA-0000'

        nfe['transporte']['valor-frete'] = nota_obj.venda.frete
        nfe['transporte']['valor-seguro'] = nota_obj.venda.seguro
        nfe['transporte']['peso-bruto'] = nota_obj.venda.peso_bruto
        nfe['transporte']['peso-liquido'] = nota_obj.venda.peso_liquido
        nfe['transporte']['quantidade-volume'] = nota_obj.venda.volumes
        nfe['transporte']['especie_volume'] = nota_obj.venda.especie_transporte
        nfe['transporte']['marca_volume'] = nota_obj.venda.marca_transporte

        itens = []

        for index, item in enumerate(nota_obj.venda.itens_venda.all(), 1):
            produto = {
                'produto': item.produto.codigo,
                'quantidade': item.quantidade,
                'valor-unitario': item.valor_unit
            }

            itens.append(produto)




