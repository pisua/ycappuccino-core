import { Routes } from '@angular/routes'
import { MatchListComponent } from './resources/matches/match-list/match-list.component'
import { MatchDetailComponent } from './resources/matches/match-detail/match-detail.component'

export const appRoutes: Routes = [
  {
    path:'',
    component : MatchListComponent
  },
  {
    path:'',
    component : MatchDetailComponent
  }
]
