#--------------------------------------------------------------------------------------------------------------------
# Test function to Create Transaction
#--------------------------------------------------------------------------------------------------------------------

def test_create_transaction(client):
    payload = {
        "title": "Movie night",
        "amount": 500,
        "type": "expense",
        "category": "Entertainment",
        "date": "2026-02-01",
    }
    response = client.post("/transactions", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Movie night"
    assert data["amount"] == 500
    assert data["type"] == "expense"
    assert data["category"] == "Entertainment"
    assert "id" in data
    assert "owner_id" in data








#--------------------------------------------------------------------------------------------------------------------
# Test function to get transactions for logged in user 
#--------------------------------------------------------------------------------------------------------------------

def test_get_all_transactions(client, sample_transaction):
    response = client.get("/transactions")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == sample_transaction.title






#--------------------------------------------------------------------------------------------------------------------
# Test function to get transactions by id for logged in user
#--------------------------------------------------------------------------------------------------------------------

def test_get_transaction_by_id(client, sample_transaction):
    response = client.get(f"/transactions/{sample_transaction.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_transaction.id
    assert data["title"] == sample_transaction.title
    assert data["category"] == sample_transaction.category








#--------------------------------------------------------------------------------------------------------------------
# Test function to test missing transaction 
#--------------------------------------------------------------------------------------------------------------------

def test_get_transaction_by_id_not_found(client):
    response = client.get("/transactions/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Transaction not found"







#--------------------------------------------------------------------------------------------------------------------
# Test function to update transactions for logged in user
#--------------------------------------------------------------------------------------------------------------------

def test_update_transaction(client, sample_transaction):
    update_payload = {"amount": 300, "category": "Groceries"}
    response = client.put(f"/transactions/{sample_transaction.id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 300
    assert data["category"] == "Groceries"
    assert data["title"] == sample_transaction.title  







#--------------------------------------------------------------------------------------------------------------------
# Test function to delete transactions for logged in user
#--------------------------------------------------------------------------------------------------------------------

def test_delete_transaction(client, sample_transaction):
    response = client.delete(f"/transactions/{sample_transaction.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Transaction deleted successfully"

    # confirm it's actually gone
    follow_up = client.get(f"/transactions/{sample_transaction.id}")
    assert follow_up.status_code == 404