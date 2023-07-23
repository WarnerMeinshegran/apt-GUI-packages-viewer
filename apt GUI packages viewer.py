# a gui interface to display apt packages

# Imports
import PySimpleGUI as sg
from subprocess import check_output,Popen,PIPE
from re import search, IGNORECASE
import json
from os.path import exists

# Program related variables
name = "apt GUI packages viewer"
version = "1.0"
author = "blabla_lab"

GIF_LOADING = b"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"
GIF_LOADING2 = b"R0lGODlhoACgAHAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQJDQAAACwAAAAAoACgAIEAAAAAAAD5wwsAAAAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoeBZQaHiImKi4yIgo1wgZKXn4OGl5SRmHuWlZyfnJ6FkoQFpqeoqaqmrqqHm4ChsL2wqHKHuLK0D7Zpvrq7rr1vtLXBrcNlxMfMyWrOzLvOb8jButNk0ta52GnT2bWfu6+vltKBpQjpkecL5uud4+zgnvaug+SR9u7527jdbNL5U/QuICagPHq6DBfAn3LWQoTOFDgQgjOpxI0Vy93FEYgVVEJrGjsY/NQorURVKaSZEDzQDE2LLMy4kxycx8WHPMzYU5xew02DPMz4BBwQzlV/TLUW9JvSzN1rTLU2pRuUx9VnXLVWVZtWwt1jXL12Upr4E6m+gc2rNq135q63YT3LiXBtm9izev3r18+/r9Cziw4MGECxs+jDix4sWMGzt+DDmy5MmUK1u+jDmz5s2cO3v+LIOuRruiC+Etze4u6tOl8SIt2+f16EGyTd+tndoubtdMYfPZfbv3bEHAdQu3TRqfvOGB3i1HPsi5R+aApGeELsg6qrBsCgAAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAA+cMLAAAAAv6Ej6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKHgWUGh4iJiouMiIKNcIGSl5+DhpeUkZh7lpWcn5yehZKEBaanqKmqpq6qh5uAobC9sKhyh7iytA+2ab66u669b7S1wa3DZcTHzMlqzsy7zm/IwbrTZNLWudhp09m1n7uvr5bSgaUI6ZHnC+brnePs4J72roPkkfbu+du43WzS+VP0LiAmoDx6ugwXwJ9y1kKEzhQ4EIIzqcSNFcvf5RGIFVRCaxo7GPzUKK1EVSmkmRA80AxNiyzMuJMcnMfFhzzM2FOcXsNNgzzM+AQcEM5Vf0y1FvSb0szda0y1NqUblMfVZ1y1VlWbVsLdY1y9dlKa+BOpvoHNqzatd+aut2E9y4lwbZvYs3r969fPv6/Qs4sODBhAsbPow4seLFjBs7fgwZCl1JfCZHqmy5EebMizZzTrvnJEqNekSHFWO67JzUpPOwLsTnNbvQJ0+HkR27tmo5uGmP3ATxzily8lrjGT6vOGzfpIh7NC6cVfLny0vrhm6nt3WWu+Nod329Onju2Ot8Px5+9vaOtsGcj05ePPr46sez7w7nffb0fAIKAAAh+QQJDQAAACwAAAAAoACgAIEAAAAAAAD5wwsAAAAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoeBZQaHiImKi4yIgo1wgZKXn4OGl5SRmHuWlZyfnJ6FkoQFpqeoqaqmrqqHm4ChsL2wqHKHuLK0D7Zpvrq7rr1vtLXBrcNlxMfMyWrOzLvOb8jButNk0ta52GnT2bWfu6+vltKBpQjpkecL5uud4+zgnvaug+SR9u7527jdbNL5U/QuICagPHq6DBfAn3LWQoTOFDgQgjOpxI0Vy9/lEYgVVEJrGjsY/NQorURVKaSZEDzQDE2LLMy4kxycx8WHPMzYU5xew02DPMz4BBwQzlV/TLUW9JvSzN1rTLU2pRuUx9VnXLVWVZtWwt1jXL12Upr4E6m+gc2rNq135q63YT3LiXBtm9izev3r18+/r9CxgDXbRzB0sqbBgS4sShNjLu5PgkqrBYxv6ifMUytLLcVnbEbEVzP87/PMMkTfCiZJQa9XFcTQp0FdHVULs0TdO2TNPk5LVu+DqjOt+F4nncBBGk6lO9jxePTPxS8pLLT8qmQvvW9SnZD/62GHz1dindY42PUn66yuosddvEjdO9Tvg85fukD9S+UPxEW/Ub5Y+Uf0oByJSAThEIlYFSIUiVglYxiJWDWkHIlYReUQiWhWJhSNZ3yoUn2XlQpBedcbCJ+ASJzrEDHWysPecaOi6+yGKMjx3m2I2RLKajhpX1OAmPQNb4RgEAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAA+cMLAAAAAv6Ej6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKHgWUGh4iJiouMiIKNcIGSl5+DhpeUkZh7lpWcn5yehZKEBaanqKmqpq6qh5uAobC9sKhyh7iytA+2ab66u669b7S1wa3DZcTHzMlqzsy7zm/IwbrTZNLWudhp09m1n7uvr5bSgaUI6ZHnC+brnePs4J72roPkkfbu+du43WzS+VP0LiAmoDx6ugwXwJ9y1kKEzhQ4EIIzqcSNFcvf5RGIFVRCaxo7GPzUKK1EVSmkmRA80AxNiyzMuJMcnMfFhzzM2FOcXsNNgzzM+AQcEM5Vf0y1FvSb0szZYUlFRFLJ5Sizo1a6GqKzti1TqV68WTpL6CBSWWI9mRGi2cDbvC6jOz6Nay3Rr3LdoLcpU15av3E4a+xf66DcxpcFeYKUkgTgx4LFnDFR5vUiz5JGUthJc15raY5ud/oXGOJpiZ5WmXi8nJa9tQbUZ1r/Hqk43KtUfYFnGf0j2b3ca6u2kXF36buN3NWTr/Yo7FObTVMkvzpG7TOlDsOrUT5e7TO1LwQsUzJW/UPFT0StVfZe/U/Vz4XaT3o8/FfjX8W23034J+hX8H8QZSal7xx5l8fiHYnIKFMRidg54RWJKBjFGokoWiYXiNhM9BGKCH03EImoamkUiaidehiJplk5zjIiQwxhjKcDTWmNyNiwzCY48+/ghkkEIOSWSRRh6JZJJKLslkk04+CWWUghQAACH5BAkNAAAALAAAAACgAKAAgQAAAAAAAPnDCwAAAAL+hI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCh4FlBoeIiYqLjIiCjXCBkpefg4aXlJGYe5aVnJ+cnoWShAWmp6ipqqauqoebgKGwvbCocoe4srQPtmm+uruuvW+0tcGtw2XEx8zJas7Mu85vyMG602TS1rnYadPZsJAiquKNJN+vltWD7OXrhumI4ZH/DeLl4fMG85j2/Pia9vEr8Q/sYBXIUOIbgP5ryl2oahocNTEC9InGhsoYf+ixh1aezAEWNFCyEnjqxQ0uFJCim9rZzQMttLCTGpzYxQ89lNCDmV7XzQs9hPB0GXfeRQ9NfQBkmhHd3QNNdSBlGrPdVQ9dbUBVm1Xc3QMCGwrxFfdYy1VUFYTgPDmT2rUB3Btw/ZxnU3Fx7cu/TyjuK7j+/BvXXlutU7dlNbhnQJsyJrsbHjc5BJSp6cNkFXtJVRXnacGcHmxRs/Ew59YLRgv/kmU+zM0vRe1AZUJ8Z7+K/rjIYZI97tsXfp37tpA7BdGLdv3cCNI0flXDbc6MRdU2deHDZM6WevtwYeXPnwgv9Yg6csHCT5T4Oba6e5vnzu7+7TI42/qX12+1CF8WPSb917YTz3Gn/XcNeRcVQQ+JiB3CAokoBgMMibeMhAaJKEX1CInoXNYKiShl5wGF5ftfh3iSgoRqLiio206OIiMMaYyCA23ohjjjruyGOPPv4IZJBCDklkkUYeiWSSSi7JZJNOPglllFJOSWWVVl6JZZZabslll15+CWaYYo5JphEFAAAh+QQJDQAAACwAAAAAoACgAIEAAAAAAAD5wwsAAAAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoeBFQaHiImKi4yIgo0ggZKXn4OGl5SRmCuWlZyfnJ6Ak6mglCemooigqqusrZ6oqpKkBba3uLm6tr66h5uAscDNxr+it8jEz8gYjcHKzswew8jQvdIU2dLWDNga09zb3h/d0crjFOfmyegZ7+XLps7J4MHy0/L7yO0Y6fq094r9+ufxb4CeRV71rAg9USdlvIEGEqX4YiDnQoDqLF/m0Yz2m0SLCCQY6bhnVk95EkJpMTi1W8WBJmoVkyL7GcSbHQTZs1aer6tNOnP05BcwbYaamoS501k/Y0inSS0ngvN94KSWEkQ6wTtB7kKsGrQLARxPYjC8EsPrQP1M5j68CtO7gN5Kajy8AuObwL9H7jq8CvNsAJBGcjjMAwNcQHFIM7uS/lVsgAq1qtxdiAY2eZAWwuR7mg5K+hRY4eWzrr6bOpu65e2zrs67exy86eWzvt7bu52+7e2zvu77/B6w4fXDzv8cPJ+y5f3Dzw88ctqTK9jDl64emctSfmDrq6PcvYO3+mJ14h+cvmwaPHufQo9uzpH6632v7+xvzXlufzlz+fSgEIVZ53jbmnjoGaIZiPgp4x+E59GekHkoPnJSihR7F8AsuGk3ToYSQghtjIiCQuYuKJiaSoooUtfmjUi6HEKKMig9yIY4467shjjz7+CGSQQg5JZJFGHolkkkouyWSTTj4JZZRSTklllVZeiWWWWm7JZZdefglmmGKOSWaZZp6JZppqrslmm26+CWeccpZQAAAh+QQJDQAAACwAAAAAoACgAIEAAAAAAAD5wwsAAAAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoOEhYaHiImKi4yNjo+AgZKTkJGGB5iZmpucnZmSniGSo6iglKeopaGpLKemraCtv5GkurClKLezmbG7vL2+r7m7orUGx8jJysvHz8uYrJHC0d7XwLPY2dXf2Rme0tve3R/U2eHN4xXq4ucM6Rvk7evvEO7y2vQV+PfZ+Rrw9ui9u1f9oCihtIcBo/DP4SKlt4oaFDZBAtSJxorGKF/osY2RlEh7CjuY/uQopsRnKeyZPFNFLgiNHlhIuwqKXEtzJjK5u6nl3imQpoAGLMaha92S9ny51He1r72TRo1KE+LQk9JZToMqNbkTJU6pFV1qoBrpIa+9Qqy5FOBUJdi7Ltwbdwl8oFSbeuTAkwJ+6N0NfhXwiBEw5+UJjgYQeJ/y1u0FjfYwaR601eUBneZQWZ121O0FndZwShy40+UDqe14hgO542kPrbawCx7a222Drm7Y25/e5+2Vvw75nBDQ/nW1zxccDJHS8n3Fzyc8TRLU9nXF3zdcjZPW+n3F30d8zhTY/nXF713ZJ54c6uXXC9yvZr36eXfR70fdvyknHSZ2nffycFqFZddlmilYEElmXggVSlxWCDCzboYIJ65UfafvEhSBaFYXEIoYcTUjiihBiiJkwvZKWISjAsjuLii6HEKKMsK9Y444042gjhjp7Q6OOJsAUpCiVGHolkkkouyWSTTj4JZZRSTklllVZeiWWWWm7JZZdefglmmGKOSWaZZp6JZppqrslmm26+eUcBACH5BAkNAAAALAAAAACgAKAAgQAAAAAAAPnDCwAAAAL+hI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCg4SFhoeIiYqLjI2Oj4CBkpOUlZaXmJmam5ydnp+QkaKjpKWmp6ipqqusrauhMAGys7S1trezsrgrvL2yur6xss/BsybBwMfKx8m7zsTAzyLB3bPL1cbX2MnT1cLfANHi4+Tl4enlssa77Ovo4erd4uP//+MTuPz17vcZ/vP76vQ79/BAUE5DCwoL+DGxIqxMdQg8OH8iJmmEhRHzT+e/Ey0tvIr6PHdhYxYBxJruSFkyjFqbTAsiW4lxViyjQIUqDImwBzItzJ85zPhkCDfqNJwaZMpBNiKnM3VGLRmcegUksXy+owrQG8mXv6NerFqUerhr0KL+vZrWu7YoXFNRhXr+XA1hVrkixOY3PfBojrq29auEZ7ouWotrDQwyETKy7LWKfjx0wlKG1ZOcJllJkhbB7Z+cFnj6EdjM5YusFpiqkZrH7YesFrhbEVzC5YO8FtgrkR7P7X+8DvhXhX6r0Z3MDwfMkBLIdYHObxpdFrTsdcPel1ztmbbgfd3fJ30uE1j0dd3vN51ulFr4fd3vR72vFVz8dd3/V93vmSZe8H3p9t/xEX2U+TKdbccx8VSNSBhSU4IHMB6hYhdAxK5aBREGYY1IaEPQYZLHSB6OFfIIbo1mAmnljiiSiOSNmEvlW4oIh+ubiXjSri2KKLPbIoo3DcXOPXkMJsY2QvSCa5y5JMMlPkk01GKSWUKlaJi5NYBqnclry4AmaYYo5JZplmnolmmmquyWabbr7ZZgEAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAA+cMLAAAAAv6Ej6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKDhIWGh4iJiouMjY6PgIGSk5SVlpeYmZqbnJ2en5CRoqOkpaanqKmqq6ytrq+gobKztLW2t7i5uru8vb6/sLHCw8jBVgfIycrLzM3Jws4hwtPY0MTX2NXR2SzX1t3Q3e/B1Org1Sjn48nh6+zt7t/p69LlBvf4+fr79//7yNzC+gwID+zgEciDBhwQ/JEjoUuNBDw4cU80XsMLGiRv4BFzlk3Eix44aPIB2K1ECyJMKTGVKqhGiO4cGXCmNKnElzIEsMLnPq23mhp098QC0IHWqvaIWjSDnaxIizqcWnHqNK7Ud1pNWr9ZRSYIrU64Sj4AhmRbk1aTez6v4dY5sNbgB6/MrWPdsybde1d9safNs3buC5bo3JvSaX7j67i/Hy1OuUW+LCAQ5Tm/zXMNepfmUC3oy1883PoPeKhkq6tFgJYIeujtDa52sIsXPOflCb5m0HuV/ubtBb5W8GwUsOX1Ac5HEFyTcuT9Bc43ME0StOP1A9pOOgkJteN5D94XcA4U1uN9o97Pml6V2v/9pe9vux8W3PZ11f933Y+XJ976fdn3D/4RagcQPyVqByBwKXoHMLEtegdA8iF6F1EzJXoXanVZUaaOOVV9OGWnW42YcZinchdCeaJyJaJHJl4otXxahZaaYZo5iNNFZm442EZcZjjzv26GOOqqVI3Yoh4kgZkZExCaSTQxI5pZB4FQAAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAA+cMLAAAAAv6Ej6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKDhIWGh4iJiouMjY6PgIGSk5SVlpeYmZqbnJ2en5CRoqOkpaanqKmqq6ytrq+gobKztLW2t7i5uru8vb6/sLHCw8TFxsfIycrLzM3Oz8DB0tPQ0WYH2Nna29zd2dLeIdLj6ODU5+jl4eks5+bt4O3/0eT68OUo9/PZ8fv8/f7u9fun0CCho8iDChwoUHv63DxjCixIgO70GciDFjxdAP2TJ6lLjRQ8ePJBOG7DCypEoBJzmkXEmy5YaXMD3K1ECzJsabGXLqBGmP48WfGoOKHEp0Ik8MPpMqXHqhqVOEUC1InWqwaoWrWFkaRYm0q8mvLsOKbUh2ptmzBbVS4IrV7YSr8Cimxbk2azu7+h5e45sOcACCDOsWvtszb9u9h/ta/Ns4cOTBfq0JPieY8ELDmxEzVeyVXebKAS6TG/3YMtuxjoVCXo229dHXsBfLBku7tlwJcKfujtDb6W8IwZMOf1Cc6HEHyX8ub9BcJ88CACH5BAkNAAAALAAAAACgAKAAgQAAAAAAAAAAAAAAAALIhI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCg4SFhoeIiYqLjI2Oj4CBkpOUlZaXmJmam5ydnp+QkaKjpKWmp6ipqqusra6voKGys7S1tre4ubq7vL2+v7CxwsPExcbHyMnKy8zNzs/AwdLT1NXW19jZ2tvc3d7f0NHi4+Tl4+WwAAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAAAAAAAAAAAvyEj6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKDhIWGh4iJiouMjY6PgIGSk5SakUcImZqbnJeWnYCRqK+SlauklqmhqAqlrK2hr6CtspO3taaCtamzuKy0vr+3tLKMy5+3vMm5y7bNs8+wwb3VpZbX2Nna29zd3t/Q0eLj5OXm5+jp6uvs7e7v4OHy8/T19vf4+fr7/P3+//DzCgwIEECxo8iDChwoUMGzp8CDGixIkUK1oUUwAAIfkECQ0AAAAsAAAAAKAAoACBAAAAAAAAAAAAAAAAAv6Ej6nL7Q+jnLTai7PevPsPhuJIluaJpurKtu4Lx/JM1/aN5/rO9/4PDAqHxKLxiEwql8ym8wmNSqfUqvWKzWq33K73Cw6Lx+Sy+YxOq9fstvsNj8vn9Lr9js/r9/y+/w8YKDhIWGh4iJiouMjY6GgXECk5SVlpeTnJh7nJuanZCRr6GUqKOVqKmrmXyip52lr6Ciu6Oosqa8uJm2taywu6+1sZLKyqV9xJjBygjNxc/Cwc/TvNW517bZs9uw3b3frNGp46fuu7bPmovs7e7v4OHy8/T19vf4+fr7/P3+//DzCgwIEECxo8iDChwoUMGzp8CDGixIkUK1q8iDGjxhONHDt6/AgypMiRJEuaPIkyJZoCACH5BAkNAAAALAAAAACgAKAAgQAAAAAAAAAAAAAAAAL+hI+py+0Po5y02ouz3rz7D4biSJbmiabqyrbuC8fyTNf2jef6zvf+DwwKh8Si8YhMKpfMpvMJjUqn1Kr1is1qt9yu9wsOi8fksvmMTqvX7Lb7DY/L5/S6/Y7P6/f8vv8PGCg4SFhoeIjoF7DI2Oj4CBkp6Sg3aXmJ2ViZydmpGecZyrkpWipJapr6CafayojqagobKzpL62l7OwqqW5rbe/kLPCk8HFls/IicvPrGvMv6jLksTf1szYydrG3MPewNDN4rrkt+a06LHqvuyt7qrgqfKi/LK21J72t/f7rPD5kooMCBBAsaPIgwocKFDBs6fAgxosSJFCtavIgxo8YrjRw7evwIMqTIkSRLmjyJMqXKlSxbunwJM6bMmTRr2ryJM6fOnTx7+pRSAAAh+QQJDQAAACwAAAAAoACgAIEAAAAAAAAAAAAAAAAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoeBZQaHiImKi4yIgo1wgZKXn4OGl5SRmHuWlZyfnJ6Ak6mglHemooigqqusrZ6ooJG9upSfs5exuZq9vI27v4C5woPFz6ZlxrmixZzOycDG0sPUwNbN2Lrat9y03rHQvuKr5Kjmp+ik6qPsrOassM6Y4LHx9ab684/4qf79jvLxXAgAH2bTIoa2BAhJcYKkNGkNigiRQrWryIMaPGPY0cO3r8CDKkyJEkS5o8iTKlypUsW7p8CTOmzJk0a9q8iTOnzp08e/r8CTSo0KFEixo9ijSp0qVMmzolUQAAOw=="


# Variables
raw_packages_installed = check_output(["apt", "list", "--installed"]).splitlines()
x = []
CACHE_FILE_NAME = "PACKAGES CACHE.json"


# ui configs
sg.theme_add_new(
    'AppThemeGray', 
    {
        'BACKGROUND': '#3f3f3f', 
        'TEXT': '#fcfcfc', 
        'INPUT': '#ccc', 
        'SCROLL': '#333', 
        'TEXT_INPUT': '#191919', 
        'BUTTON': ('#fcfcfc', '#b2b2b2'), 
        'PROGRESS': ('#ccc', '#4c4c4c'), 
        'BORDER': 0, 
        'SLIDER_DEPTH': 0, 
        'PROGRESS_DEPTH': 0, 
    }
)

sg.theme('AppThemeGray')

def scan_installed_packages(cache_file = False, ui = True, update_key_when_no_ui=None):
    global total_installed_packages, packages
    x = []
    if cache_file is True and exists(cache_file) is True:
        with open(CACHE_FILE_NAME, "r") as cache_file:
            packages = json.load(cache_file)
            total_installed_packages = len(packages.keys())
    else:
        raw_packages_installed = check_output(["apt", "list", "--installed"]).splitlines()
        total_installed_packages = len(raw_packages_installed)
        for line in raw_packages_installed:
            if ui:
                sg.one_line_progress_meter("Decoding packages...",raw_packages_installed.index(line), total_installed_packages, no_button=True, no_titlebar=True,)
            elif update_key_when_no_ui is not None:
                exec(update_key_when_no_ui + f".update('{raw_packages_installed.index(line)}/{total_installed_packages}')")
            
            x.append(line.decode())
            
        sg.one_line_progress_meter_cancel()
        
        sg.popup_animated(None)
        raw_packages_installed = x
        
        raw_packages_installed.pop(0)
        
        total_installed_packages = len(raw_packages_installed)
        packages = {}
        for package in raw_packages_installed:
            total_installed_packages = len(raw_packages_installed)
            packages[package.split("/")[0]] = package.split("/")[1].replace("[installed]", "").replace("installed", "").replace("local", "")
            if ui:
                sg.one_line_progress_meter("Organizing packages...", raw_packages_installed.index(package), total_installed_packages, no_button=True, no_titlebar=True)
            elif update_key_when_no_ui is not None:
                exec(update_key_when_no_ui + f".update('{raw_packages_installed.index(package)}/{total_installed_packages}')")
        
        sg.one_line_progress_meter_cancel()
        with open(CACHE_FILE_NAME, "w") as cache_file:
            json.dump(packages, cache_file,indent=2)
        sg.popup_animated(None)


if exists(CACHE_FILE_NAME) is True:
    scan_installed_packages(True)
else:
    scan_installed_packages()


print(packages)



layout = [  [sg.Text("Packages", font=(None, 16), enable_events=True, key="-TITLE-", tooltip="Click me for settings")],
            [sg.Frame("Search", [
                [sg.Input("", expand_x=True, key="-SEARCH-", enable_events=True), sg.B("Cancel search",
                                                                                        key="-CANCEL SEARCH-",
                                                                                        disabled=True)],[sg.T(f"{total_installed_packages} packages",key="-STATUES-")]],)],
            [sg.B("Refresh", expand_x=True)],
            [sg.Listbox(packages.keys(),
                        size=(40,20),
                        expand_x=True,
                        expand_y=True,
                        select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                        key="-PACKAGES-",
                        enable_events=True)],
            [sg.T("Selected package:"), sg.T(key="-SELECTED PACKAGE-"), sg.B("About this package"), sg.B("Remove package")],
        ]

window = sg.Window('Packages', layout, resizable=True).finalize()

window["-PACKAGES-"].update(values = packages.keys())

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == "Refresh":
        window.perform_long_operation(lambda: scan_installed_packages(ui=False, update_key_when_no_ui="window['-STATUES-']"), "-REFRESHED-")
        window["-PACKAGES-"].update(disabled=True)

        
    elif event == "-REFRESHED-":
        window["-PACKAGES-"].update(values = packages.keys())
        window["-PACKAGES-"].update(disabled=False)
        window["-SEARCH-"].update("")
        window["-STATUES-"].update(f"{total_installed_packages} packages")
        window.write_event_value("-CANCEL SEARCH-", "")
        
    
    
    elif event == "-SEARCH-":
        found_packages = []
        if values["-SEARCH-"].strip() == "":continue
        
        window["-STATUES-"].update("Searching...")

        
        for package_name in list(packages.keys()):
            result = search(values["-SEARCH-"], package_name, flags=IGNORECASE)
            if result is None:
                continue
            else:
                found_packages.append(result.string)
        
        # if nothing is found
        
        
        window["-STATUES-"].update(f"found {len(found_packages)} packages")
        window["-PACKAGES-"].update(values = found_packages)
        window["-CANCEL SEARCH-"].update(disabled=False)

    elif event == "-CANCEL SEARCH-":
        window["-PACKAGES-"].update(values = packages.keys())
        window["-CANCEL SEARCH-"].update(disabled=True)
        window["-STATUES-"].update(f"{total_installed_packages} packages")
        
    elif event == "-PACKAGES-":
        selected_package = "".join(values["-PACKAGES-"])
        window["-SELECTED PACKAGE-"].update(selected_package)
    elif event == "About this package":
        try:
            sg.popup_scrolled(check_output(["apt", "show", selected_package]).decode(), title = "About package")
        except NameError:continue
    elif event == "Remove package":
        try:
            if sg.popup_yes_no(f"Remove package:\n{selected_package}?").lower() == "yes":
                pass
            else: raise AttributeError
        except AttributeError:
            sg.popup_quick_message(f"Aborted removal of {selected_package}")
            continue
        except NameError:
            sg.popup_quick_message("Select a package first")
            continue
        else:
            try:
            
                output_window = sg.Window("Output",
                                          [
                                          [sg.T(f"Removing {selected_package}")],
                                          [sg.Multiline("", disabled=True, key="output", size=(80,30))],
                                          ]).finalize()
                output = []
                with Popen(f"pkexec apt remove -y {selected_package}", shell=True, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                    for line in p.stdout:
                        output_window.refresh()
                        print(line, type(line))
                        output.append(str(line))
                        output_window["output"].update(line)
                
                
                output_window.close()

                        
                                
            except KeyboardInterrupt as e:
                sg.popup_error(f"Error occured\n{e}\n\nThis probably happened because\nyour system doens't have apt or pkexec\n or you just didnt enter your password")
            
        
        
        
    print(event, values)
    

window.close()
