---
description: Her geliştirmeden sonra otomatik git push yap (develop + main)
---

// turbo-all

Her kod değişikliği yapıldıktan sonra aşağıdaki adımları sırayla uygula:

1. Değiştirilen dosyaları stage'e al:
```
git add <değiştirilen dosyalar>
```

2. Açıklayıcı bir commit mesajı ile commit et:
```
git commit -m "feat/fix/refactor: kısa açıklama"
```

3. develop branch'e push et:
```
git push origin develop
```

4. main branch'e de push et:
```
git push origin develop:main
```

> NOT: Her geliştirme tamamlandıktan hemen sonra bu adımlar uygulanmalı, kullanıcının görmesi beklenmemelidir.
