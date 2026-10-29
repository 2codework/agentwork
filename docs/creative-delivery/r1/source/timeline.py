"""Pure half-open interval exercise. Not a media renderer or interchange standard."""

def transform_item(item, track):
    a,b=item['start_ms'],item['end_ms']
    if not (type(a) is int and type(b) is int and 0<=a<b<=24000):
        raise ValueError('INVALID_INTERVAL')
    if track=='captions' and ((a<8000<b) or (a<12000<b)):
        raise ValueError('CAPTION_EDIT_REQUIRES_AUTHORING')
    result=[]
    for number,(left,right,offset) in enumerate(((0,8000,0),(12000,24000,4000)),1):
        start,end=max(a,left),min(b,right)
        if start>=end: continue
        source_start=item['source_start_ms']+start-a
        result.append(dict(fragment_id=f"{item['item_id']}.k{number}",original_id=item['item_id'],asset_id=item['asset_id'],start_ms=start-offset,end_ms=end-offset,source_start_ms=source_start,source_end_ms=source_start+end-start,text=item['text']))
    return result
