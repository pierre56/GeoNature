import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Role } from './form.service';

import { ConfigService } from '@geonature/utils/configModule/core';

@Injectable()
export class UserDataService {
  public API_ENDPOINT: string;
  constructor(private _http: HttpClient, private _configService: ConfigService) {
    this._configService.getSettings('API_ENDPOINT');
  }

  getRole(id: number) {
    return this._http.get<any>(`${this.API_ENDPOINT}/users/role/${id}`);
  }

  getRoles(params?: any) {
    let queryString: HttpParams = new HttpParams();
    // tslint:disable-next-line:forin
    for (let key in params) {
      if (params[key] !== null) {
        queryString = queryString.set(key, params[key]);
      }
    }
    return this._http.get<any>(`${this.API_ENDPOINT}/users/roles`, { params: queryString });
  }

  putRole(role: Role): Observable<Role> {
    const options = role;
    return this._http.put<any>(`${this.API_ENDPOINT}/users/role`, options).pipe(
      map((res: Role) => {
        return res;
      })
    );
  }

  putPassword(role: Role): Observable<any> {
    const options = role;
    return this._http.put<any>(`${this.API_ENDPOINT}/users/password/change`, options).pipe(
      map((res: Role) => {
        return res;
      })
    );
  }
}
