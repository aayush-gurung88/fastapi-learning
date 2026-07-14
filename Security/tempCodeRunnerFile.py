
    if not author:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not found")
    
    return author
