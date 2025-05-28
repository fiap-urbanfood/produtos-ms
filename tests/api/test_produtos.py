import pytest
from fastapi import status
from httpx import AsyncClient

from models.produtos_models import ProdutosModel

@pytest.mark.asyncio
async def test_criar_produto(client):
    produto_data = {
        "nome": "Teste Produto",
        "categoria": "Teste Categoria",
        "preço_unitario": 10.99
    }
    
    response = await client.post("/api/v1/produtos/", json=produto_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["nome"] == produto_data["nome"]
    assert data["categoria"] == produto_data["categoria"]
    assert data["preço_unitario"] == produto_data["preço_unitario"]
    assert "id" in data

@pytest.mark.asyncio
async def test_listar_produtos(client, db_session):
    # Criar alguns produtos de teste
    produtos = [
        ProdutosModel(nome="Produto 1", categoria="Categoria 1", preço_unitario=10.99),
        ProdutosModel(nome="Produto 2", categoria="Categoria 2", preço_unitario=20.99)
    ]
    for produto in produtos:
        db_session.add(produto)
    await db_session.commit()

    response = await client.get("/api/v1/produtos/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["nome"] == "Produto 1"
    assert data[1]["nome"] == "Produto 2"

@pytest.mark.asyncio
async def test_buscar_produto_por_id(client, db_session):
    # Criar um produto de teste
    produto = ProdutosModel(nome="Produto Teste", categoria="Categoria Teste", preço_unitario=15.99)
    db_session.add(produto)
    await db_session.commit()

    response = await client.get(f"/api/v1/produtos/{produto.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["nome"] == "Produto Teste"
    assert data["categoria"] == "Categoria Teste"
    assert data["preço_unitario"] == 15.99

@pytest.mark.asyncio
async def test_buscar_produto_inexistente(client):
    response = await client.get("/api/v1/produtos/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_atualizar_produto(client, db_session):
    # Criar um produto de teste
    produto = ProdutosModel(nome="Produto Original", categoria="Categoria Original", preço_unitario=10.99)
    db_session.add(produto)
    await db_session.commit()

    produto_atualizado = {
        "nome": "Produto Atualizado",
        "categoria": "Categoria Atualizada",
        "preço_unitario": 20.99
    }

    response = await client.put(f"/api/v1/produtos/{produto.id}", json=produto_atualizado)
    assert response.status_code == status.HTTP_202_ACCEPTED
    data = response.json()
    assert data["nome"] == produto_atualizado["nome"]
    assert data["categoria"] == produto_atualizado["categoria"]
    assert data["preço_unitario"] == produto_atualizado["preço_unitario"]

@pytest.mark.asyncio
async def test_deletar_produto(client, db_session):
    # Criar um produto de teste
    produto = ProdutosModel(nome="Produto para Deletar", categoria="Categoria Teste", preço_unitario=10.99)
    db_session.add(produto)
    await db_session.commit()

    response = await client.delete(f"/api/v1/produtos/{produto.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar se o produto foi realmente deletado
    response = await client.get(f"/api/v1/produtos/{produto.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND 