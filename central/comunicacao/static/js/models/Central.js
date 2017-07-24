class Central {
	constructor(_dados) {
		try {			
			if (_dados.empresa) this.empresa = _dados.nomeFantasia;
			if (_dados.descricao) this.descricao = _dados.descricao;
			this.id = _dados.id;
		}
		catch (err) {
			return(err);
		}
	}
}