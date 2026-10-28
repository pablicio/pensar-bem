@router.get("/versao")
def versao():
    return {"versao": VERSAO, "commit": COMMIT, "build": BUILD_EM}
