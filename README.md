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
    "schedule": 
      {
            "time":"int"
            "runtime":"int"
            "loop": "bool"
            "isStarting": "bool"
      }
}
```
- `time`: thời gian sự kiện diễn ra (giây)
- `runtime`: thời gian còn lại của sự kiện được khởi tạo bằng time (giây)
- `loop`: sự kiện có lặp lại hay không
- `isStarting`: có đang diễn ra hay không
## mô tả `API`
- `creating`: tạo 1 chiến dịch mới và gọi điện thông báo cho các khách hàng lấy từ `customer_data` về sự bắt đầu
- `update`: nhận vào 1 id và thay đổi đặc điểm của chiến dịch
- `starting`: bắt đầu 1 chiến dịch với `id` cho trước: set lại `isStarting`: **True** bắt đầu giảm runtime từng giây bằng cách `update` liên tục 
- `stoping`: dừng 1 chiến dịch với `id` cho trước: set lại  `isStarting`: **False** dùng quá trình liên tục gọi `update` (có thể start lại)
- `duplicate`: kích hoạt vòng lặp `loop`: **True** khi runtime = 0 gán lại runtimr = time
- `disabling`: vô hiệu chiến dịch gán time = runtime = 0 từ đó không thể start chiến dịch

## docker
```
docker built -t managecampaigns
```


