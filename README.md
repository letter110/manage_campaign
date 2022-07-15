# manage_campaign
## mô tả `data`
``` json
{
    "id": "uuid"
    "name": "string"
    "customer_data": [
        {
            "name": "string",
            "phone_number": "string",
            "any": "string",
        }
    ]
}
```

## mô tả `API`
- `creating`: tạo 1 chiến dịch mới 
- `update`: nhận vào 1 id và thay đổi đặc điểm của chiến dịch
- `starting`: bắt đầu 1 chiến dịch với `id` cho trước
- `stoping`: dừng 1 chiến dịch với `id` cho trước:
- `duplicate`: tạo 1 chiến dịch mới giống với chiến dịch theo id đã cho
- `disabling`: xóa chiến dịch

## docker
```
docker built -t managecampaigns
```


